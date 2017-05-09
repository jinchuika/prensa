import feedparser
from bs4 import BeautifulSoup
from time import mktime
from datetime import datetime

from django.db import IntegrityError

from news.models import NewsSource, Article


class NewsParser(object):

    def get_sources(self):
        return NewsSource.objects.all()

    def get_articles(self, feed_url):
        feed_content = feedparser.parse(feed_url)
        return feed_content

    def create_articles(self, article_list):
        for article in article_list['items']:
            art = Article(
                link=article.link,
                title=BeautifulSoup(article.title, "html.parser").get_text(),
                summary=BeautifulSoup(article.published, "html.parser").get_text(),
                parsed=datetime.fromtimestamp(mktime(article.published_parsed)),
                published=datetime.strptime(article.published, "%a, %d %b %Y %X %z"),
                enclosure=article.enclosures[0].href)
            art.save()

    def parse_feed(self):
        source_list = NewsSource.objects.all()
        for source in source_list:
            feed_content = feedparser.parse(source.feed_url)
            for article in feed_content['items']:
                try:
                    new_article = Article(
                        link=article.link,
                        title=BeautifulSoup(article.title, "html.parser").get_text(),
                        summary=BeautifulSoup(article.published, "html.parser").get_text(),
                        parsed=datetime.fromtimestamp(mktime(article.published_parsed)),
                        published=datetime.strptime(article.published, "%a, %d %b %Y %X %z"),
                        enclosure=article.enclosures[0].href)
                    new_article.save()
                except IntegrityError:
                    pass
                print(new_article)
