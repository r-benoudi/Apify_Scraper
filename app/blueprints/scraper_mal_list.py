import json
import json
from json import dumps
import requests
import os
from sys import stdout
import random
from bs4 import BeautifulSoup
import time

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

def scrape_agent(url, payload={"limit":0}):
    # result = {}
    user_agents = users_agents()
    headers = {
        'User-Agent': random.choice(user_agents), 
        # "Accept": "text/html,application/xhtml+xml,application/xml,apllication/json;q=0.9,image/avif,image/webp,*/*;q=0.8",
        # "Accept-Language": "en-US,en;q=0.5",
        # "Accept-Encoding": "gzip, deflate",
        # "Connection": "keep-alive",
        # "Upgrade-Insecure-Requests": "1",
        # "Sec-Fetch-Dest": "document",
        # "Sec-Fetch-Mode": "navigate",
        # "Sec-Fetch-Site": "none",
        # "Sec-Fetch-User": "?1",
        # "Cache-Control": "max-age=0"
        }
    response = requests.get(url, headers=headers, params=payload)
    soup = BeautifulSoup(response.content,"html.parser")
    # href
    # image
    # title
    # manga vol | ans | members
    # score
    manga_details= {}
    
    data = soup.find_all("tr", class_="ranking-list")

    for num, val in enumerate(data):
        manga_details[str(num + payload["limit"])] = {
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
    # result = scrape_agent(url="https://myanimelist.net/topmanga.php", payload={"limit": 50})

    results = {}
    for i in range(1611,1614):
        print(f"Link Scraped {i}")
        result = scrape_agent(url="https://myanimelist.net/topmanga.php", payload={"limit": i*50})
        results |= result

    output(results,f"tmp/3_result_data_all.json")
    # print("sleep")
    # time.sleep(2)
    # output(results,f"result_data_all.json")

        

    


