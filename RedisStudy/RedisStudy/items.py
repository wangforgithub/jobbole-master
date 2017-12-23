import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from RedisStudy.utils.common import *
from w3lib.html import remove_tags


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(remove_space)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    contents = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole(title, url, url_object_id, front_image_url, create_date, fav_nums, praise_nums, comment_nums, tags, contents)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        front_image_url = ""

        if self["front_image_url"]:
            front_image_url = self["front_image_url"][0]
        params = (self["title"], self["url"], self["url_object_id"], self["front_image_url"],self["create_date"], self["fav_nums"],
                    self["praise_nums"], self["comment_nums"], self["tags"], self["contents"])

        return insert_sql, params