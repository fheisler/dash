class Item():
    def __init__(self, title, url, source, body, date):
        self.title = title
        self.url = url
        self.source = source
        self.body = body
        self.date = date
    def setRank(self, rank):
        self.rank = rank

class NewsArticle(Item):
    def __init__(self, title, url, source, body, date):
        Item.__init__(self, title, url, source, body, date)
        self.type = "article"

class Event(Item):
    def __init__(self, title, url, source, body, date):
        Item.__init__(self, title, url, source, body, date)
        self.type = "event"
