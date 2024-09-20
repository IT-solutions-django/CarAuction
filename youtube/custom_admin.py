from django.contrib import admin
from django import forms
from django.db import transaction
from django.http import JsonResponse
from youtube.models import Chanel, PlayList, Video, ChannelPlayList
from django.urls import path
import re
from youtube.youtube_api import PlayListApi, VideoApi


class YouTubeChannelAdminForm(forms.ModelForm):
    selected_playlist = forms.ModelChoiceField(queryset=PlayList.objects.none(), required=False,
                                               label="Выберите плейлист")

    class Meta:
        model = Chanel
        fields = ('url',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['selected_playlist'].queryset = self.instance.playlists.all()


class YouTubeChannelAdmin(admin.ModelAdmin):
    change_form_template = 'change_form_admin.html'
    form = YouTubeChannelAdminForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:
            video_object = VideoApi

            request = video_object.get_playlist_items(
                playlist_id=form.cleaned_data.get('selected_playlist').playlist_id)
            response = request.execute()

            is_shorts = 'shorts' in form.cleaned_data.get('selected_playlist').name.lower()

            video_titles = []

            for item in response['items']:
                video_data = {
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'video_id': item['snippet']['resourceId']['videoId']
                }

                if is_shorts:
                    video_data['url_shorts'] = f'https://www.youtube.com/shorts/{video_data["video_id"]}'

                video_titles.append(video_data)

            video_ids = [video_data['video_id'] for video_data in video_titles]

            existing_videos = Video.objects.filter(video_id__in=video_ids)
            existing_video_dict = {video.video_id: video for video in existing_videos}

            video_to_update = []
            new_video = []

            for video in video_titles:
                title = video['title']
                description = video['description']
                id_video = video['video_id']

                if id_video in existing_video_dict:
                    existing_video = existing_video_dict[id_video]
                    if existing_video.title != title or existing_video.description != description:
                        existing_video.title = title
                        existing_video.description = description
                        video_to_update.append(existing_video)
                else:
                    new_video.append(
                        Video(
                            title=title,
                            description=description,
                            video_id=id_video,
                            url_shorts=video.get('url_shorts', None)
                        )
                    )

            with transaction.atomic():
                if new_video:
                    created_videos = Video.objects.bulk_create(new_video)
                    all_videos = created_videos + list(existing_videos)
                else:
                    all_videos = list(existing_videos)

                if video_to_update:
                    Video.objects.bulk_update(
                        video_to_update,
                        ['title', 'description']
                    )

                form.cleaned_data.get('selected_playlist').video.add(*all_videos)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'load-playlists',
                self.admin_site.admin_view(self.load_playlists_view),
                name='load-playlists',
            ),
        ]

        return urls + custom_urls

    def load_playlists_view(self, request):
        playlist_object = PlayListApi

        pattern_url_youtube = r'^(https?://)?(www\.)?(youtube\.com/(c|channel|user|@)[\w-]+/?|youtu\.be/[\w-]+)$'

        url_channel = request.GET['url']

        if not re.match(pattern_url_youtube, url_channel):
            return JsonResponse({'detail': 'Проверьте ссылку на корректность'}, status=400,
                                json_dumps_params={'ensure_ascii': False})

        channel_id = url_channel.split('/')[-1]

        if channel_id[0] == '@':
            search_response = playlist_object.get_channel_id(channel_id)

            items = search_response.get('items', [])

            if items:
                channel_id = items[0]['id']['channelId']
            else:
                return JsonResponse({'detail': 'Канал не найден'}, status=404,
                                    json_dumps_params={'ensure_ascii': False})

        channel_response = playlist_object.get_channel(channel_id)

        if 'items' not in channel_response or not channel_response['items']:
            return JsonResponse({'detail': 'Канал не найден'}, status=404, json_dumps_params={'ensure_ascii': False})

        channel, _ = Chanel.objects.update_or_create(
            url=url_channel
        )

        playlists_response = playlist_object.get_playlist(channel_id)

        playlist_ids = [playlist['id'] for playlist in playlists_response['items']]

        existing_playlists = PlayList.objects.filter(playlist_id__in=playlist_ids)
        existing_playlists_dict = {playlist.playlist_id: playlist for playlist in existing_playlists}

        playlists_to_update = []
        new_playlists = []

        for playlist in playlists_response['items']:
            playlist_id = playlist['id']
            playlist_title = playlist['snippet']['title']

            if playlist_id in existing_playlists_dict:
                existing_playlist = existing_playlists_dict[playlist_id]
                if existing_playlist.name != playlist_title:
                    existing_playlist.name = playlist_title
                    playlists_to_update.append(existing_playlist)
            else:
                new_playlists.append(
                    PlayList(
                        playlist_id=playlist_id,
                        name=playlist_title
                    )
                )

        with transaction.atomic():
            if playlists_to_update:
                PlayList.objects.bulk_update(playlists_to_update, ['name'])

            if new_playlists:
                created_playlists = PlayList.objects.bulk_create(new_playlists)
                all_playlists = created_playlists + list(existing_playlists)

            else:
                all_playlists = list(existing_playlists)

            existing_channel_playlists = set(ChannelPlayList.objects.filter(channel=channel,
                                                                            playlist__in=all_playlists).values_list(
                'playlist_id', flat=True))
            ChannelPlayList.objects.bulk_create([
                ChannelPlayList(channel=channel, playlist=playlist)
                for playlist in all_playlists
                if playlist.id not in existing_channel_playlists
            ])

        return JsonResponse({'detail': 'Плейлисты успешно загружены'}, status=200,
                            json_dumps_params={'ensure_ascii': False})


class PlayListAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'playlist_id')
    fields = ('name', 'playlist_id')


class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ('title', 'description', 'video_id', 'url_shorts')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('playlists')


class ChannelPlayListAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('channel', 'playlist')
