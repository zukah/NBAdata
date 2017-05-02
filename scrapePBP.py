#scrapePBP.py

from bs4 import BeautifulSoup
from urllib2 import urlopen
import requests
import csv
import os

# This is a test comment, added on Work Mac and committed via Github 5/2/2017

#game_id = "201503020MIA"

def write_PBP_row(writer,ROW_TYPE,QTR,TIME,GENERAL_EVENT,AWAY_EVENT,SCORE,HOME_EVENT):
    writer.writerow([ROW_TYPE,QTR,TIME,GENERAL_EVENT,AWAY_EVENT,SCORE,HOME_EVENT])

def scrape_PBP_data(game_id):

    BASE_URL = "http://www.basketball-reference.com/boxscores/pbp/"+game_id+".html"
    
    html = urlopen(BASE_URL).read()
    soup = BeautifulSoup(html, 'html5lib')
    
    stats_table = soup.find("table","no_highlight stats_table")
    rows = stats_table.find_all("tr")
    
    output_path = os.getcwd()+"\\Scraped PBP\\"+game_id+" - Parsed.csv"
    #output_path = "C:/Users/ezuk/Desktop/PYTHON/NBA data scraping/Game output/201503020MIA.csv"
    
    csv_file = open(output_path, "wb")
    writer = csv.writer(csv_file, delimiter = ',')
    
    header_row = ['ROW_TYPE','QTR','TIME','GENERAL_EVENT','AWAY_EVENT','SCORE','HOME_EVENT']
    
    writer.writerow(header_row)
    
    #want to store the data in the following format
    #ROW_TYPE: either "PLAY" or "INFO"
    #QTR: quarter of the game
    #TIME: the time left in the quarter
    #GENERAL_EVENT: text not specific to one team
    #AWAY_EVENT: any text related to an away team event
    #SCORE: the score of the game
    #HOME_EVENT: any text related to a home team event
    
    current_qtr = "q1"
    
    output_row = []
    
    #process each tr
    for row in rows:
    
        if str(row.get('id')).startswith("q"):
            current_qtr = row.get('id')
            write_PBP_row(writer,'INFO',str(current_qtr),None,None,None,None,None)
            continue
        
        td_list = row.findAll("td")
        
        #print "*** BEGIN NEW ROW ***"
        #print "length of row is "+str(len(td_list))
        #for td in td_list:
            #print td
        #print "*** END ROW ***"
            
        if len(td_list)== 0:
            continue
        elif len(td_list) == 2:
            current_time = td_list[0].renderContents().strip()
            current_general_event = td_list[1].renderContents().strip()
            write_PBP_row(writer,'INFO',str(current_qtr),current_time,current_general_event,None,None,None)
        elif len(td_list) == 6:
            #print td_list
            current_time = td_list[0].renderContents().strip()
            current_away_event = td_list[1].renderContents().strip()
            current_score = td_list[3].renderContents().strip()
            current_home_event = td_list[5].renderContents().strip()
            write_PBP_row(writer,'PLAY',str(current_qtr),current_time,None,current_away_event,current_score,current_home_event)
        else:
            print "There is an error row that is "+str(len(td_list))+" tds long"
            print row
    
    csv_file.close()

