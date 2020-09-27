import scrapy
from ..items import ScrapWinesItem


class WinesComSpider(scrapy.Spider):
    name = 'wines_com'
    allowed_domains = ['wine.com']
    start_urls = [
        'https://www.wine.com/list/wine/7155?pricemax=200&ratingmin=98',  # test subset
        # 'https://www.wine.com/list/wine/white-wine/7155-125'
        # 'https://www.wine.com/list/wine/red-wine/7155-124',
    ]

    IMAGE_URL_PREFIX = 'https://wine.com'

    def parse(self, response):
        for wine in response.css('.prodItem_wrap'):
            image_urls = wine.css('img.prodItemImage_image-default::attr(src)').get()
            wine_url = wine.css("a.prodItemInfo_link::attr(href)").get()

            wine_data = ScrapWinesItem(
                wine_url=wine_url,
                title=self.extract_text_from_span(wine, "prodItemInfo_name"),
                rating=self.extract_text_from_span(wine, "averageRating_average"),
                varietal=self.extract_text_from_span(wine, "prodItemInfo_varietal"),
                origin=self.extract_text_from_span(wine, "prodItemInfo_originText"),
                num_ratings=self.extract_text_from_span(wine, "averageRating_number"),
                price=self.extract_text_from_span(wine, "productPrice_price-regWhole"),

                tags=tuple(
                    t.css("::attr(title)").get() for t in wine.css('ul.prodAttr>li')
                ),
                image_urls=[(self.IMAGE_URL_PREFIX + image_urls)] if image_urls else []
            )

            yield response.follow(
                wine_url,
                callback=self.parse_wine_page,
                cb_kwargs={'item': wine_data}
            )

        for next_page in response.css('a.listPageNextUrl'):
            yield response.follow(next_page, self.parse)

    def parse_wine_page(self, response, item):
        description = response.css(
            '.pipWineNotes .viewMoreModule_text *::text'
        ).extract()
        alc_percentage = self.extract_text_from_span(
            response, "prodAlcoholPercent_percent"
        )
        item.update(
            description=description, alc_percentage=alc_percentage
        )

        yield item

    def extract_text_from_span(self, response, class_name):
        return response.css(f'span.{class_name}::text').get()
