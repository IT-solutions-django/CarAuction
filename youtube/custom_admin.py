from django.contrib import admin
from django import forms
from django.db import transaction
from django.http import HttpResponse
from youtube.models import Chanel, PlayList, Video
from django.urls import path
import re
from youtube.youtube_api import PlayListApi, VideoApi


class YouTubeChannelAdminForm(forms.ModelForm):
    class Meta:
        model = Chanel
        fields = ('url',)


class YouTubeChannelAdmin(admin.ModelAdmin):
    change_form_template = 'change_form_admin.html'
    form = YouTubeChannelAdminForm

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
            return HttpResponse('Проверьте ссылку на корректность', status=400)

        channel_id = url_channel.split('/')[-1]

        if channel_id[0] == '@':
            search_response = playlist_object.get_channel_id(channel_id)

            items = search_response.get('items', [])

            if items:
                channel_id = items[0]['id']['channelId']
            else:
                return HttpResponse('Канал не найден', status=404)

        channel_response = playlist_object.get_channel(channel_id)

        if 'items' not in channel_response or not channel_response['items']:
            return HttpResponse('Канал не найден', status=404)

        channel, _ = Chanel.objects.update_or_create(
            url=url_channel
        )

        playlists_response = playlist_object.get_playlist(channel_id)

        existing_playlists = PlayList.objects.filter(chanel=channel).values('playlist_id', 'id')
        existing_playlists_dict = {playlist['playlist_id']: playlist['id'] for playlist in existing_playlists}

        playlists_to_update = {playlist_id: {'id': playlist_id, 'name': ''} for playlist_id in existing_playlists_dict}
        new_playlists = []

        for playlist in playlists_response['items']:
            playlist_id = playlist['id']
            playlist_title = playlist['snippet']['title']

            if playlist_id in playlists_to_update:
                playlists_to_update[playlist_id]['name'] = playlist_title
            else:
                new_playlists.append(
                    PlayList(
                        playlist_id=playlist_id,
                        name=playlist_title,
                        chanel=channel
                    )
                )

        playlists_to_update_objects = [
            PlayList(id=existing_playlists_dict[playlist_id], name=data['name'])
            for playlist_id, data in playlists_to_update.items()
        ]

        with transaction.atomic():
            if playlists_to_update:
                PlayList.objects.bulk_update(playlists_to_update_objects, ['name'])
            if new_playlists:
                PlayList.objects.bulk_create(new_playlists)

        return HttpResponse('Плейлисты успешно загружены', status=200)


class PlayListAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'playlist_id', 'chanel')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:
            video_object = VideoApi

            request = video_object.get_playlist_items(playlist_id=obj.playlist_id)
            response = request.execute()

            video_titles = []

            for item in response['items']:
                video_titles.append({
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description']
                })

            existing_video = Video.objects.filter(playlist=obj).values('title', 'id', 'description')
            existing_video_dict = {video['title']: {'id': video['id'], 'description': video['description']} for
                                   video in existing_video}

            video_to_update = {}
            new_video = []

            for video in video_titles:
                title = video['title']
                description = video['description']

                if title in existing_video_dict:
                    video_id = existing_video_dict[title]['id']
                    video_to_update[video_id] = {
                        'title': title,
                        'description': description
                    }
                else:
                    new_video.append(
                        Video(
                            title=title,
                            description=description,
                            playlist=obj
                        )
                    )

            video_to_update_objects = [
                Video(id=video_id, title=data['title'], description=data['description'])
                for video_id, data in video_to_update.items()
            ]

            with transaction.atomic():
                if new_video:
                    Video.objects.bulk_create(new_video)
                if video_to_update_objects:
                    Video.objects.bulk_update(
                        video_to_update_objects,
                        ['title', 'description']
                    )


class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ('title', 'description', 'playlist')
