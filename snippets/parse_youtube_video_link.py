# !title: Get the embed code & thumbnails for the YouTube video
# !date: 2012-04-13
# !tags: Django, Video
# !author: Denis Veselov

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _ 


class Video(models.Model):

    title = models.CharField(_('title'), max_length=200)
    url = models.CharField(_('YouTube Video URL'), max_length=250)

    def get_video_id(self):
        id = None
        if 'youtu.be' in self.url.lower():
            id = re.search(r'be/([A-Za-z0-9\-_]+)[#&]{0,1}.{0,}$',
                           self.url, re.DOTALL)
            if id:
                id = id.groups()[0]
        if 'youtube.com' in self.url.lower():
            id = re.search(r'v=([^&]+)[#&]{0,1}.{0,}$', self.url, re.DOTALL)
            if id:
                id = id.groups()[0]
        return id

    def get_big_video_thumbnail(self):
        id = self.get_video_id()
        if id:
            return 'http://i.ytimg.com/vi/' + id + '/0.jpg'
        return ''

    def get_small_video_thumbnail(self):
        id = self.get_video_id()
        if id:
            return 'http://i.ytimg.com/vi/' + id + '/1.jpg'
        return ''

    def get_embed_code(self):
        id = self.get_video_id()
        if id:
            return '<iframe width="640" height="360" src="http://www.youtube' +
                   '.com/embed/%s" frameborder="0" allowfullscreen>' +
                   '</iframe>' % self.get_video_id()
        return ''
