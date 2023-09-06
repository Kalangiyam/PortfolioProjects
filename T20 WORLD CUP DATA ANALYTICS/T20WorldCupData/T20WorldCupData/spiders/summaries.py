# First let's import the packages we will use in this project

import scrapy
import pandas as pd
from datetime import datetime
import re

# For Match
teamf=[]
teams=[]
margin=[]
ground=[]
date=[]
match_1=[]
winner=[]


# For Batsman
match=[]
teaming_bat=[]
battingor=[]
batt=[]
run=[]
ball=[]
four=[]
six=[]
srs=[]
outs=[]
match_no=[]
matchno=[]

# For Bowler
teaming_bow=[]            
bow=[]
over=[]
maiden=[]
wickets=[]
economy=[]
zes=[]
fos=[]
sixb=[]
wides=[]
noBalls=[]
runb=[]
wic=[]
match_bow=[]
matchnob=[]


class Level2Spider(scrapy.Spider):
    name = "summaries"
    allowed_domains = ["www.espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2022-23-1298134/namibia-vs-sri-lanka-1st-match-first-round-group-a-1298135/full-scorecard"]

    def parse(self, response):
        infon=response.xpath('//div[contains(@class,"ds-text-tight-m ds-font-regular ds-text-typo-mid3")]/text()').get()
        match_1.append(infon.split(",")[0].strip(' (N)'))
        if infon is not None:
            if 'Final' in infon:                
                ground.append(infon.split(",")[1].strip())
                date.append(datetime.strptime(((infon.split(",")[2].strip())+" "+(infon.split(",")[3].strip())), '%B %d %Y').strftime('%d-%b-%Y'))
            else: 
                ground.append(infon.split(",")[2].strip())
                date.append(datetime.strptime(((infon.split(",")[3].strip())+" "+(infon.split(",")[4].strip())), '%B %d %Y').strftime('%d-%b-%Y'))
        
       
        team=response.xpath('//div[contains(@class,"r-1")]/a/span/text()').getall()
        for n, teamg in enumerate(team):
            if n==0 :
                teamf.append(teamg)
            else:
                teams.append(teamg)   

        win=response.xpath('//p[contains(@class,"m")]/span/text()').get()
        win=re.sub(r'\([^)]*\)', '', win).strip()
        winn=(win.split(" "))

    # This section collect winner and margin data
        if win in ["No result", "Match abandoned without a ball bowled"]:
                winner.append(win)
                margin.append("  -  ")
        else:
            n=len(winn)            
            if n==6:
                winner.append(winn[0]+" "+winn[1])
                margin.append(winn[4]+" "+winn[5])               
                               
            else:
                winner.append(winn[0])
                margin.append(winn[3]+" "+winn[4])

    # Batsman  & Bowler data
        if 'Match abandoned' not in win: 
            for n in range(4):
                tbody=response.xpath('//div/table/tbody')[n]
                
                if n in [0,3]:
                    t=0 # Represents the index of the first team
                    o=1 # Represents player batting position
                else:
                    t=1 # Represents the index of the second team
                    o=1

            # Batsman data                
                if n==0 or n==2:
                    batsman=tbody.xpath('.//tr/td[1]/div/a/span/span/text()[1]').getall() 
                    
                    runs=tbody.xpath('.//tr[@class=""]/td[3]/strong/text()').getall()
                
                    balls=tbody.xpath('.//tr/td[4]/text()').getall()
                    fours=tbody.xpath('.//tr/td[6]/text()').getall()
                    sixs=tbody.xpath('.//tr/td[7]/text()').getall()
                    sr=tbody.xpath('.//tr/td[8]/text()').getall()               
                    for n in range(len(batsman)):
                        teaming_bat.append(team[t])
                        match.append(team[0]+" vs "+team[1])
                        battingor.append(o)
                        o+=1
                        batt.append(batsman[n].strip())
                        run.append(runs[n].strip())
                        ball.append(balls[n].strip())
                        four.append(fours[n].strip())
                        six.append(sixs[n].strip())
                        srs.append(sr[n].strip())
                        out=tbody.xpath('.//tr[@class=""]/td[contains(@class,"x !")]')[n].xpath('.//text()').get().strip()
                        if out=='not out':
                            outs.append(out)
                        else:
                            outs.append('out')
                        matchno.append(response.xpath('//div[contains(@class,"r ds-t")]/text()[1]').get().split(',')[0].strip(' (N)'))
                       
                        
            # Bowlers data      
                else:                
                    bowlerName=tbody.xpath('.//tr/td[1]/div/a/span/text()').getall()                
                    overs=tbody.xpath('.//tr/td[2]/text()').getall()
                    maidens=tbody.xpath('.//tr/td[3]/text()').getall()
                    run_bow=tbody.xpath('.//tr/td[4]/text()').getall()
                    economyb=tbody.xpath('.//tr/td[6]/text()').getall()
                    zs=tbody.xpath('.//tr/td[7]/text()').getall()
                    fs=tbody.xpath('.//tr/td[8]/text()').getall()
                    ss=tbody.xpath('.//tr/td[9]/text()').getall()
                    wide=tbody.xpath('.//tr/td[10]/text()').getall()
                    noBall=tbody.xpath('.//tr/td[11]/text()').getall()
                    for n in range(len(bowlerName)):
                        match_bow.append(team[0]+" vs "+team[1])
                        teaming_bow.append(team[t])
                        bow.append(bowlerName[n].strip())
                        over.append(overs[n].strip())
                        maiden.append(maidens[n].strip())
                        runb.append(run_bow[n].strip())
                        wickets=tbody.xpath('.//tr/td[5]')[n].xpath('.//span/strong/text()').get()
                        if wickets==None:
                            wic.append('0')
                        else:
                            wic.append(wickets)
                
                        economy.append(economyb[n].strip())
                        zes.append(zs[n].strip())
                        fos.append(fs[n].strip())                
                        sixb.append(ss[n].strip())
                        wides.append(wide[n].strip())
                        noBalls.append(noBall[n].strip())
                        matchnob.append(response.xpath('//div[contains(@class,"r ds-t")]/text()[1]').get().split(',')[0].strip(' (N)'))
                        

    # Next page url
        next_url=response.xpath('//div/a[contains(@class,"ds-group ds-inline-flex ds-items-center ds-ml-4")]/@href').get()
        
        if next_url is not None:
            url=next_url.replace('live-cricket-score','full-scorecard')
            next_page='https://www.espncricinfo.com'+url            
            yield response.follow(next_page,callback=self.parse)

    # Making csv file with pandas dataframe 
     
    # Match data
        mat= {'ground':ground,'date':date,'match':match_1,'winner':winner,'margin':margin,'team1':teamf,'team2':teams}
        m=pd.DataFrame(mat)
        m.to_csv('match_summary.csv',index=False) 

    # Bowling data
        bowf ={ 'match':match_bow,'bowlingTeam':teaming_bow,'bowlerName':bow,'overs':over, 'maiden':maiden, 'runs':runb,'wickets':wic, 'economy':economy,'0s':zes,'4s':fos,'6s':sixb,'wides':wides,'noBalls':noBalls,'match_id':matchnob}
        dfbow=pd.DataFrame(bowf)
        dfbow.to_csv('bowling_summary.csv',index=False)
                
    # Batting data
        bat={'match':match,'battingTeam':teaming_bat,'batting_pos':battingor,'batsmanName':batt,'runs':run,'balls':ball,'fours':four,'sixs':six, 'sr':srs,'out':outs,'match_no':matchno,}
        dfbat=pd.DataFrame(bat)
        dfbat.to_csv('batting_summary.csv',index=False)
        
