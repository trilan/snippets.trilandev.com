# !title: Get the embed code & thumbnails for the YouTube video
# !date: 2012-04-13
# !tags: Video, Parsing
# !author: Denis Veselov

import re


class BadVideoURL(Exception):
    pass


class YouTubeVideo(object):

    def __init__(self, url):
        self.url = url

    def get_id(self):
        if 'youtu.be' in self.url.lower():
            match = re.search(r'be/([^&#]+)[#&]{0,1}.{0,}$', self.url)
            if match:
                return match.group(1)
        if 'youtube.com' in self.url.lower():
            match = re.search(r'v=([^&#]+)[#&]{0,1}.{0,}$', self.url)
            if match:
                return match.group(1)
        raise BadVideoURL('%s it is not YouTube video URL' % self.url)

    def get_big_thumbnail(self):
        return 'http://i.ytimg.com/vi/%s/0.jpg' % self.get_id()

    def get_small_thumbnail(self):
        return 'http://i.ytimg.com/vi/%s/1.jpg' % self.get_id()

    def get_embed_code(self):
        return ('<iframe width="640" height="360" src="http://www.youtube'
                '.com/embed/%s" frameborder="0" allowfullscreen>'
                '</iframe>' % self.get_id())
