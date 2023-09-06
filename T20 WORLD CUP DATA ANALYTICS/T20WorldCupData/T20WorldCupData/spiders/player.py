# First let's import the packages we will use in this project
import scrapy

class PlayerSpider(scrapy.Spider):
    name = "player"
    allowed_domains = ["www.espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2022-23-1298134/afghanistan-squad-1334760/series-squads"]

    def parse(self, response):
         
        divs=response.xpath('//div[@class="ds-relative ds-flex ds-flex-row ds-space-x-4 ds-p-3"]')       
        
        # team name
        name1=divs.xpath('//span[@class="ds-text-title-xs ds-font-bold ds-text-typo"]/text()')[1].get()
        name2=name1.replace("squad","")
        teamName=name2.replace("Squad","").strip()

        # plyer information
        for n,div in enumerate(divs):
            playerName=div.xpath('.//a/span/text()').get().strip()
            playingRole=div.xpath('.//p/text()').get().strip()
            battingStyle=div.xpath('.//div[@class="ds-justify-between ds-text-typo-mid3"]/div[2]/span[2]/text()').get()
            bowlingStyle=div.xpath('.//div[@class="ds-justify-between ds-text-typo-mid3"]/div[3]/span[2]/text()').get()            
        
            yield {'name':playerName,'team':teamName ,'playingRole':playingRole,'battingStyle':battingStyle,'bowlingStyle':bowlingStyle}
       
        # getting team squad links
        links=response.xpath('//div[@class="ds-p-0"]/a/@href').getall()       
        for n,link in enumerate(links):
            if n>0:                
                yield response.follow(url=link, callback=self.parse)
        