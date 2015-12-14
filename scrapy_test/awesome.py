import scrapy

class StackOverflowSpider(scrapy.Spider):
	name = 'awesome'
	start_urls = ['http://marczyk.ovh/angular-blog-0.0.1/']

	def parse(self, response):
		for href in response.css('.post_title a::attr(href)'):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_post)

	def parse_post(self, response):
		yield {
			'title': response.css('.post_title::text').extract()[0],
			'author': response.css('.post_author::text').extract()[0],
			'body': response.css('.content::text').extract()[0],
			'date': response.css('.post_date::text').extract()[0],
			'link': response.url,
		}