from pygame import image

"""
This serves to make sure we don't load images more than once since
we'll be asking for images when menus initialize. This also makes it
really easy to selectively clear images from memory. (probably unnecessary)
"""
class ImageCache(object):
    cache = {}

    @staticmethod
    def add(path, alpha = False):
        if not path in ImageCache.cache:
            if alpha:
                ImageCache.cache[path] = image.load(path).convert_alpha()
            else:
                ImageCache.cache[path] = image.load(path).convert()

        return ImageCache.cache[path]