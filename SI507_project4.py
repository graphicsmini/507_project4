import requests, json
from bs4 import BeautifulSoup
from advanced_expiry_caching import Cache
import numpy as np
import pandas as pd
# "crawling" -- generally -- going to all links from a link ... like a spiderweb
# its specific def'n varies, but this is approximately the case in all situations
# and is like what you may want to do in many cases when scraping

######


# Constants
START_URL = "https://www.nps.gov/index.htm"
FILENAME = "npc_cache.json"
PROGRAM_CACHE = Cache(FILENAME)

# assuming constants exist as such
# use a tool to build functionality here
def access_page_data(url):
    data = PROGRAM_CACHE.get(url)
    if not data:
        data = requests.get(url).text
        PROGRAM_CACHE.set(url, data) # default here with the Cache.set tool is that it will expire in 7 days, which is probs fine, but something to explore
    return data

#######

main_page = access_page_data(START_URL)
main_soup = BeautifulSoup(main_page, features="html.parser")
# print(main_soup.prettify())
#
list_of_topics = main_soup.find('ul', class_='dropdown-menu SearchBar-keywordSearch')
# all_links = list_of_topics.find_all('a')
# print(all_links)
#
states_urls = []
for link in list_of_topics.find_all('a'):
    # print(link.get('href'))
    states_urls.append("{}{}".format("https://www.nps.gov",link.get('href')))
# print(states_urls)


npc_dic = {} #dictionary of lists

npc_dic['Type'] = []
npc_dic['Name'] = []
npc_dic['Location'] = []
npc_dic['Description'] = []



for url in states_urls:
    state_page = access_page_data(url)
    state_soup = BeautifulSoup(state_page, features="html.parser")
    #print(state_soup.prettify())
    # for item in state_soup.find_all("ul", {"id":"list_parks"}):
    for each_item in state_soup.find("ul", id="list_parks").find_all('li', class_="clearfix"):
        # print('===============')
        # print(each_item)
        # print('===============')

        sitetype = each_item.find('h2')
        sitename = each_item.find('h3').find('a')
        sitelocation = each_item.find('h4')
        sitedescription = each_item.find('p')

        # npc_dic['type'].append(sitetype)
        # npc_dic['name'].append(sitename)
        # npc_dic['location'].append(sitelocation)
        # npc_dic['description'].append(sitedescription)


        if (sitetype) and (sitetype.text != ""):
            npc_dic['Type'].append(sitetype.text)
        else:
            npc_dic['Type'].append("None")

        if (sitename) and (sitename.text != ""):
            npc_dic['Name'].append(sitename.text)
        else:
            npc_dic['Name'].append("None")

        if (sitelocation) and (sitelocation.text != ""):
            npc_dic['Location'].append(sitelocation.text)
        else:
            npc_dic['Location'].append("None")

        if (sitedescription) and (sitedescription.text != ""):
            npc_dic['Description'].append(sitedescription.text.strip())
        else:
            npc_dic['Description'].append("None")

        # print(npc_dic)

npc_data = pd.DataFrame.from_dict(npc_dic)
npc_data.to_csv('npc.csv')
