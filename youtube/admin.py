from django.contrib import admin
from youtube.models import Chanel, Video, PlayList, ChannelPlayList
from youtube.custom_admin import YouTubeChannelAdmin, PlayListAdmin, VideoAdmin, ChannelPlayListAdmin


admin.site.register(Video, VideoAdmin)
admin.site.register(Chanel, YouTubeChannelAdmin)
admin.site.register(PlayList, PlayListAdmin)
admin.site.register(ChannelPlayList, ChannelPlayListAdmin)
