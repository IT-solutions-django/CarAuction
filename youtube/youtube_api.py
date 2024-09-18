from googleapiclient.discovery import build
from youtube.youtube_settings import ApiKey

api_key = ApiKey.API_KEY.value

youtube = build("youtube", "v3", developerKey=api_key)


class PlayListApi:
    @staticmethod
    def get_channel_id(channel_id):
        search_response = youtube.search().list(
            part='snippet',
            q=channel_id,
            type='channel',
            maxResults=1
        ).execute()

        return search_response

    @staticmethod
    def get_channel(channel_id):
        channel_response = youtube.channels().list(
            part='snippet,contentDetails',
            id=channel_id
        ).execute()

        return channel_response

    @staticmethod
    def get_playlist(channel_id):
        playlists_response = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50
        ).execute()

        return playlists_response


class VideoApi:
    @staticmethod
    def get_playlist_items(playlist_id):
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50
        )

        return request
