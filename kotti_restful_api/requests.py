class ContentTypePredicate(object):
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'content type = %s' % self.val
    phash = text

    def __call__(self, context, request):
        return request.content_type == self.val


class CrossRequestPredicate(object):
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return "cross_request = %s" % self.val
    phash = text

    def __call__(self, context, request):
        try:
            return request.cross_request == self.val
        except:
            return False
