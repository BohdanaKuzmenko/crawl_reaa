__author__ = 'bogdana'
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import requests
import scrapy
from lxml import html
import csv

class StrySpider(CrawlSpider):

    name = "stry"
    allowed_domains = ["www.reaa.govt.nz"]
    start_urls = ["http://www.reaa.govt.nz/Pages/PublicRegisterSearch.aspx?pageNo=1&name=a&orgName=&location=&licenceNo=&itemsPerPage=25&sortExpression=0"]

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'http:\/\/www\.reaa\.govt\.nz\/Pages\/PublicRegisterSearch\.aspx\?pageNo=\d+')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        self.csvwriter = csv.writer(open('items.csv', 'a'))
        k = open("'test",'a')
        f_rows = hxs.select('//*[@id="ctl00_PlaceHolderMain_CommonQuestionsDisplayEditModePanel_Search_dvsearchresult"]/table/tr')
        for row in f_rows:
            agent_name = ' '.join(row.select('td/a/text()').extract())
            known_as = ' '.join(row.select('td[2]/text()').extract())
            company = ' '.join(row.select('td/span/text()').extract())
            suburb = ' '.join(row.select('td[4]/text()').extract())
            area = ' '.join(row.select('td[5]/text()').extract())
            url = ' '.join(row.select('td/a/@href').extract())
            if url:
                yield scrapy.Request(url,callback=self.detail_page, meta={'agent_name': agent_name,'known_as': known_as,'company': company,'suburb' : suburb,'area': area})

    def detail_page(self, response):
        hxs = HtmlXPathSelector(response)
        s_rows = hxs.select('//div[@class="searchWrapper"]/div/div/table/tbody')
        t_row = hxs.select('//div[@id="ctl00_PlaceHolderMain_Search_plnIndividualLicenceDetails"]/tbody')
        for row in s_rows:
            mail = ' '.join(row.select('div/tr[2]/td/text()').extract())
        for rows in t_row:
            lic_num = ' '.join(rows.select('tr[1]/td/text()').extract())
            cur_state = ' '.join(rows.select('tr[4]/td/text()').extract())
        self.csvwriter.writerow([response.meta['agent_name'],response.meta['known_as'],response.meta['company'],response.meta['suburb'],response.meta['area'],mail, lic_num, cur_state])
