from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from tb7_scrapper.items import DownloadItem

class DownloadSpider(CrawlSpider):
	name = "download"
	http_user = "kenji89"
	http_pass = "pass"
	allowed_domains = ["tb7.pl"]
	login_url = "http://tb7.pl/login"
	mojekonto_url = "http://tb7.pl/mojekonto/pliki"
	start_urls = [ "http://tb7.pl/mojekonto/pliki" ]

	def parse(self, response):
		self.log("Logging in...")
		yield FormRequest(self.login_url, formdata={"login":self.http_user,"password":self.http_pass}, callback=self.goto_mojekonto)

	def goto_mojekonto(self, response):
		if self.http_user in response.body:
			self.log("Logged in")
			yield Request(self.mojekonto_url, callback=self.parse_links)
		else:
			self.log("Couldn't log in")

	def parse_links(self, response):
		for sel in response.css('.list tbody tr'):
			item = DownloadItem()
			item['name'] = sel.xpath('td/a/text()').extract()[0]
			item['url'] = sel.xpath('td/a/@href').extract()[0]
			yield item