#!/usr/bin/env python
# coding: utf-8

# ## 1. Get webpage using *requests*

# In[2]:


import requests

req = requests.get('https://en.wikipedia.org/wiki/Data_science')
# req


# In[4]:


webpage = req.text
# webpage


# In[12]:


with open('wiki_ds.txt', "wb") as f:
    f.write(webpage)


# In[13]:


print(webpage)


# ## 2. Get specific contents using BeatifulSoup

# In[15]:


from bs4 import BeautifulSoup

soup = BeautifulSoup(webpage, 'html.parser')


# ### 2.1 Prettify the webpage

# In[16]:


print(soup.prettify())


# ### 2.2 Get the first paragraph

# You can try to remove "attrs" to see how it works.

# In[17]:


paragraph = soup.find_all('p')


# In[18]:


paragraph


# In[19]:


paragraph = soup.find('p', attrs={"class":False})


# In[20]:


paragraph


# ### 2.3 Get all the links in this paragraph which point to other webpages

# In[21]:


paragraph.find_all('a')


# In[22]:


paragraph.find_all('a', attrs={"title":True})


# In[23]:


data = {"title":[], "href":[]}
for link in paragraph.find_all('a', attrs={"title":True}):
    data["title"].append(link["title"])
    data["href"].append(link["href"])


# In[24]:


import pandas as pd
df = pd.DataFrame(data)


# In[25]:


df


# ## 3. Get the contents from all the webpages

# In[26]:


webpages = []
head = "https://en.wikipedia.org"
for href in data["href"]:
    link = head + href
    req = requests.get(link)
    webpage = req.text
    webpages.append(webpage)


# ## 4. Futher readings

# ### 4.1 robots.txt

# Check robots.txt of the website to find out what are allowed.

# In[27]:


req = requests.get("https://en.wikipedia.org/robots.txt")
webpage = req.text


# In[28]:


soup = BeautifulSoup(webpage, 'html.parser')
print(soup.text)


# ### 4.2 Sleep

# You would be banned, if you scrape a website too fast. Let your crawler sleep for a while after each round.

# In[29]:


import time

for i in range(5):
    time.sleep(3)
    print(i)


# ### 4.3 Randomness

# Pausing for extactly three seconds after each round is too robotic. Let's add some randomness to make your crawler looks more like a human.

# In[30]:


from random import random

for i in range(5):
    t = 1 + 2 * random()
    time.sleep(t)
    print(i)


# ### 4.4 Separate the codes for scraping from the ones for data extraction

# 1. Scraping is more vulnerable. Nothing is more annoying than your crawler breaks because of a bug in the data extraction part.  
# 2. You never know what data you would need for modeling. So keep all the webpages you obtain. 

# ### 4.5 Chrome Driver and Selenium

# These are the tools make your crawler act even more like a human.

# In[ ]:





# In[ ]:


### Sample Code


# In[31]:


# import bs4
# import requests
# from urllib2 import Request, urlopen
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# import time
# import random
# import os
# import json


# head = "https://www.indeed.com/"

# chromedriver = "/Applications/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver

# job_titles = ["data+scientist"]

# def get_soup(url):
#     """
#     This function get the beautifulsoup object of a webpage.

#     Args:
#         url (str): the link string of webpage

#     Returns:
#         soup (obj): beautifulsoup object
#     """
#     request = Request(url, headers={'User-Agent': 'Resistance is futile'})
#     response = urlopen(request)
#     return BeautifulSoup(response, "html.parser")

# def get_jobs_of_title(job_title):
#     """
#     Args:
#         job_title (str): example: 'data+scientist'

#     Returns:
#     """

#     #needed to be changed
#     num_pages = 1 #number of pages to scrape
#     page_gap_min = 3 #min sleep time between pages
#     page_gap_max = 5 #max sleep time between pages
#     job_per_page = 50 #number of jobs in one page
#     job_gap_min = 5 #min sleep time between jobs
#     job_gap_max = 6 #max sleep time between jobs

#     for i in range(num_pages): 
#         #sleep between each call
#         gap = random.uniform(page_gap_min,page_gap_max) 
#         time.sleep(gap)

#         #each page contains 50 jobs
#         tail = "jobs?q={0}&sort=date&limit={1}".format(job_title,job_per_page)
#         if i>0:
#             tail += "&start={0}".format(i*job_per_page)

#         #get link to joblist page
#         url = head+tail 
         
#         #get links to webpages of jobs on the joblist
#         job_page_links = get_job_links_from_page(url)

#         for job_page_link in job_page_links:
#             gap = random.uniform(job_gap_min,job_gap_max) 
#             time.sleep(gap)
#             data = get_info_from_job_page(job_page_link)

#             print(json.dumps(data))

# def get_job_links_from_page(url):
#     """
#     This function gets the links of the jobs on the joblist page.

#     Args:
#         url (str): link to joblist page

#     Returns:
#         job_page_links (list): list of links to the webpages of the jobs
#     """

#     job_page_links = []
#     soup = get_soup(url)
#     for item in soup.find_all("a", href=True):
#         if '/rc/clk?jk=' in str(item) and 'fccid=' in str(item):
#             link = item['href'].split("clk?")[1]
#             job_page_links.append(head+'viewjob?'+link)
#     return job_page_links

# def get_info_from_job_page(url):
#     """
#     This function get all the useful info from the job webpage.

#     Args:
#         url (str): link to job webpage

#     Returns:
#         data (dict): dictionary with keywords: 
#                      time_stamp, original_link, job_title, location, company, description
#     """
#     soup = get_soup(url)
#     data = {}
#     time_str = soup.find('div',class_='result-link-bar').find('span').getText()

#     try:
#         data["time_stamp"] = get_timestamp(time_str).strftime("%d-%m-%Y %H:%M")
#         data["job_title"] = soup.find('b', class_='jobtitle').getText()
#         data["location"] = soup.find('span', class_='location').getText()
#         data["company"] = soup.find('span', class_='company').getText()
#         data["description"] = soup.find('td',class_='snip').find('div').getText()

#         re_link = soup.find('a',class_='sl ws_label')['href'].split("&from=")[0]
#         re_link = head[:-1]+re_link
#         data["original_link"] = get_original_link(re_link)
#     except:
#         pass
#     return data

# def get_timestamp(time_str):
#     """
#     Calculate the timestamp from the time string.
    
#     Args:
#         time_str (str): time string, like '2 hours ago'

#     Returns:
#         time_stamp (obj): timestamp object
#     """
#     if 'hour' in time_str:
#         lag = int(time_str.split('hour')[0])
#         delta = timedelta(hours=lag)
#         now = datetime.utcnow().replace(second=0,minute=0)
#         return now-delta
#     else:
#         return -1

# def get_original_link(url):
#     """
#     Get the original link of the job description.
    
#     Args:
#         url (str): the link in Indeed database

#     Returns:
#         url (str): the original link to the job description
#     """
#     driver = webdriver.Chrome(chromedriver)
#     driver.get(url)
#     time.sleep(2)
#     original_url = driver.current_url
#     driver.quit()
#     return original_url


# if __name__ == "__main__":
#     get_jobs_of_title("data+scientist")


# In[ ]:


## https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3


# In[ ]:





# In[ ]:





# In[ ]:




