import json
import json
from json import dumps
import requests
import os
from sys import stdout
import random
from bs4 import BeautifulSoup
import time

# https://myanimelist.net/manga/2/Berserk

def users_agents():
    with open("app/blueprints/lib/ua.txt", "r", encoding="utf-8") as ua_file:
      user_agents = [ua.strip() for ua in ua_file.readlines() if ua.strip()]
    return user_agents

def make_request(url, payload, headers):
    try:
        response = requests.get(url, params=payload, headers=headers, timeout=10)
        # response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"An error occurred during the request:", e)
        exit()
    except ValueError:
        print(f"Invalid JSON response")
        exit()

def output(data, filename):
    data = json.dumps(data, indent=2, default=str)
    with open(filename, 'w') as f:
        f.write(data)

def scrape_agent(url):
    # result = {}
    user_agents = users_agents()
    headers = {'User-Agent': random.choice(user_agents)}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content,"html.parser")

    """
    manga_id = https://myanimelist.net/manga/25/Fullmetal_Alchemist == > is "25"
    title  =  class="h1-title"  (span)
    type   =  class="information type" (span)  or  <div class="spaceit_pad"><span class="dark_text">Type:</span> <a href="/topmanga.php?type=manga">Manga</a></div>
    scored_by  =  class="fl-l score" (div)---------|
    score  =  class="score-label score-9" (div)----|
    status = <div class="spaceit_pad"> <span class="dark_text"> Status: </span> Finished </div> "problem"
    volumes = <div class="spaceit_pad"> <span class="dark_text"> Volumes:</span> 27 </div>      "problem"
    chapters = <div class="spaceit_pad"><span class="dark_text">Chapters:</span> 116 </div>     "problem"
    start_date <div class="spaceit_pad"><span class="dark_text">Published:</span> Jul  12, 2001 to Sep  11, 2010</div>
    end_date   <div class="spaceit_pad"><span class="dark_text">Published:</span> Jul  12, 2001 to Sep  11, 2010</div>
    members  <span class="numbers members">Members <strong>317,185</strong></span>  or  <div class="spaceit_pad"><span class="dark_text">Members:</span> 317,185</div>
    favorites  <div class="spaceit_pad"><span class="dark_text">Favorites:</span> 31,101</div>
    sfw       ????
    approved  ????
    created_at_before  ????
    updated_at         ????
    real_start_date	real_end_date  <div class="spaceit_pad"><span class="dark_text">Published:</span> Jul  12, 2001 to Sep  11, 2010</div>
    
    genres  <div class="spaceit_pad">
                    <span class="dark_text">Genres:</span>
                            <span itemprop="genre" style="display:none">Action</span>
            <a href="/manga/genre/1/Action" title="Action">
                Action</a>,                    <span itemprop="genre" style="display:none">Adventure</span>
            <a href="/manga/genre/2/Adventure" title="Adventure">
                Adventure</a>,                    <span itemprop="genre" style="display:none">Award Winning</span>
            <a href="/manga/genre/46/Award_Winning" title="Award Winning">
                Award Winning</a>,                    <span itemprop="genre" style="display:none">Drama</span>
            <a href="/manga/genre/8/Drama" title="Drama">
                Drama</a>,                    <span itemprop="genre" style="display:none">Fantasy</span>
            <a href="/manga/genre/10/Fantasy" title="Fantasy">
                Fantasy</a>            </div>
    
    themes  <div class="spaceit_pad">
                    <span class="dark_text">Theme:</span>
                            <span itemprop="genre" style="display:none">Military</span>
            <a href="/manga/genre/38/Military" title="Military">
                Military</a>            </div>
    demographics
    authors
    serializations
    synopsis
    background
    main_picture
    url	title_english
    title_japanese
    title_synonyms
    """

    manga_details= {}
    
    data = soup.find_all("tr", class_="ranking-list")

    for num, val in enumerate(data):
        manga_details[str(num)] = {
            "title" : val.find("a", class_="hoverinfo_trigger fs14 fw-b").text,
            "url" : val.find("a", class_="hoverinfo_trigger fs14 fw-b")['href'],
            "image" : val.find("img")['data-src'],
            "info" : val.find("div", class_="information di-ib mt4").text,
            "score" : val.find("div", class_="js-top-ranking-score-col top-ranking-score-col di-ib al").text,
        }

    # print(manga_details)
    # data_score = soup.find_all("td", class_="score ac fs14")
    

        


    # with open("test.txt", "w") as f:
    #     f.write(str(soup))
    # data = json.loads(manga_details)
    # output(manga_details,f"result_data_50.json")
    return manga_details

if __name__ == '__main__':
    # max manga 80650 / 50 = 1613
    result = scrape_agent(url="https://myanimelist.net/manga/2/Berserk")

        

    


