class JobPosting(object):
    __slots__ = ('url', 'title', 'description', '_keyword_matches')

    def __init__(self, url, title, description, keyword_matches):
        self.url = url
        self.title = title
        self.description = description
        self._keyword_matches = keyword_matches

    def __str__(self):
        return self.title

    def hasNoMatches(self):
        return not self._keyword_matches

    @property
    def keyword_matches(self):
        return ', '.join('{k}: {v}'.format(k=word, v=count) for word, count in self._keyword_matches.items())

