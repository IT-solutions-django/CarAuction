from celery import shared_task
from django.db import transaction

from youtube.youtube_api import VideoApi
from youtube.models import Chanel, PlayList, Video, ChannelPlayList


@shared_task
def load_video_for_playlists():
    playlists = PlayList.objects.all()
    video_api = VideoApi

    for playlist in playlists:
        request = video_api.get_playlist_items(playlist.playlist_id)
        response = request.execute()

        is_shorts = 'shorts' in playlist.name.lower()

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
        existing_video_ids = {video.video_id: video for video in existing_videos}

        new_videos = []
        update_videos = []

        for video_data in video_titles:
            video_id = video_data['video_id']
            if video_id not in existing_video_ids:
                new_videos.append(Video(
                    title=video_data['title'],
                    description=video_data['description'],
                    video_id=video_id,
                    url_shorts=video_data.get('url_shorts', None)
                ))
            else:
                existing_video = existing_video_ids[video_id]
                if (existing_video.title != video_data['title'] or
                        existing_video.description != video_data['description']):
                    existing_video.title = video_data['title']
                    existing_video.description = video_data['description']
                    update_videos.append(existing_video)

        with transaction.atomic():
            if new_videos:
                created_videos = Video.objects.bulk_create(new_videos)
                all_videos = list(existing_videos) + created_videos
            else:
                all_videos = list(existing_videos)

            if update_videos:
                Video.objects.bulk_update(update_videos, ['title', 'description'])

            playlist.video.add(*all_videos)
