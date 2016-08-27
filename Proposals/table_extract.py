from selenium import webdriver
from BeautifulSoup import BeautifulSoup
driver = webdriver.Firefox()
url = 'http://www.pro-football-reference.com/boxscores/201602070den.htm'
driver.get(url)
soup = BeautifulSoup(driver.page_source)
stats_table = soup.findAll('table')
for s in stats_table:
    try:
        if s.find('caption').getText() == 'Team Stats Table':
                trs = s.findAll('tr')
                for tr in trs:
                        try:
                                print tr.find('th').getText(), '***', tr.findAll('td')[0].getText(), '*****', tr.findAll('td')[1].getText()
                        except:
                                pass
    except Exception,e:
            pass

	
## *** First Downs *** 11 ***** 21
##Rush-Yds-TDs *** 28-90-1 ***** 27-118-1
##Cmp-Att-Yd-TD-INT *** 13-23-141-0-1 ***** 18-41-265-0-1
##Sacked-Yards *** 5-37 ***** 7-68
##Net Pass Yards 
##*** 104 ***** 197
##Total Yards *** 194 ***** 315
##Fumbles-Lost *** 3-1 ***** 4-3
##Turnovers *** 2 ***** 4
##Penalties-Yards *** 6-51 ***** 12-102
##Third Down Conv. *** 1-14 ***** 3-15
##Fourth Down Conv. *** 0-0 ***** 0-0
##Time of Possession *** 27:13 ***** 32:47
