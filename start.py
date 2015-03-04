import scrapePBP

from bs4 import BeautifulSoup
from urllib2 import urlopen
import requests
import csv
import os

current_year = "2015"
current_month = "3"
current_day = "2"

box_score_url = "http://www.basketball-reference.com/boxscores/index.cgi?month="+current_month+"&day="+current_day+"&year="+current_year

html = urlopen(box_score_url).read()
soup = BeautifulSoup(html, 'html5lib')

#all of the game ids can be found in the "final" links

game_ids = []

games_div = soup.find("div",attrs={'id':'boxes'})
links = games_div.find_all("a")

for link in links:
    if link.contents[0] == "Final":
        #pull out everything between the last slash and '.html'
        current_game_id = os.path.splitext(os.path.basename(link['href']))[0]
        game_ids.append(str(current_game_id))
        

for game_id in game_ids:
    scrapePBP.scrape_PBP_data(game_id)

#stats_table = soup.find("table","no_highlight stats_table")
#rows = stats_table.find_all("tr")





#scrapePBP.scrape_PBP_data("201503020MIA")
#scrapePBP.scrape_PBP_data("201503020DAL")
