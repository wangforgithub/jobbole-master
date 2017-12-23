from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from urllib import parse
from RedisStudy.items import ArticleItem, ArticleItemLoader
from scrapy.loader import ItemLoader
from RedisStudy.utils.common import get_md5


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    redis_key = 'jobbole:start_urls'

    def parse(self, response):
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), \
                          callback=self.parse_detail, meta={'front_image_url': image_url})
        # 提取下一页并交给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        print(next_url)
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass

    def parse_detail(self, response):
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=ArticleItem(), response=response)

        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("contents", "div.entry")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])

        article_item = item_loader.load_item()
        yield article_item
