from django.contrib import admin
from youtube.models import Chanel, Video, PlayList
from youtube.custom_admin import YouTubeChannelAdmin, PlayListAdmin, VideoAdmin


admin.site.register(Video, VideoAdmin)
admin.site.register(Chanel, YouTubeChannelAdmin)
admin.site.register(PlayList, PlayListAdmin)
