'''
Date: 2020-09-05
Author: Ali Eddeb

Goal: Retrieve jobs from freelancer.com
'''

#Import libraries  
import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

#list to save all data (include header)
header = ['job_title', 'description', 'url', 'tags',  'price', 'avg_bid', 'bids', 'days_remaining', 'verified_payment', 'promotions', 'contest']
job_list = [header]

#going through pages to get data

for page_num in tqdm(range(1,378)):

    #Getting page html
    url = f'https://www.freelancer.com/jobs/{page_num}/?languages=en'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    jobs = soup.find_all('div', attrs = {'class' : 'JobSearchCard-item'})

    #-------------------------------------------------------------------------------------------

    for job in jobs:
        #Get info for each job
        job_title = job.find('a', attrs = {'class' : 'JobSearchCard-primary-heading-link'}).text.replace('\n','').strip()
        if 'Private project or contest' in job_title:
            continue
        description = job.find('p', attrs = {'class' : 'JobSearchCard-primary-description'}).text.replace('\n','').strip()
        url = job.find('a', attrs = {'class' : 'JobSearchCard-primary-heading-link'})['href'] 

        tags_section = job.find_all('a', attrs = {'class' : 'JobSearchCard-primary-tagsLink'}) 
        tags = []
        for tag in tags_section:
            tag_text = tag.text
            tags.append(tag_text)

        #either range or avg. bid 
        price = job.find('div', attrs = {'class' : 'JobSearchCard-secondary-price'}).text.replace('\n','').replace('Avg Bid','').strip()

        avg_bid =  job.find('span', attrs = {'class' : 'JobSearchCard-secondary-avgBid'})
        if avg_bid != None:
            avg_bid = True
        else:
            avg_bid = False

        #bids can also represent number of entries if the job is a contest
        bids = job.find('div', attrs = {'class' : 'JobSearchCard-secondary-entry'}).text
        days_remaining = job.find('span', attrs = {'class' : 'JobSearchCard-primary-heading-days'}).text
        #bolean
        verified_payment = job.find('div', attrs = {'class' : 'JobSearchCard-primary-heading-status Tooltip--top'})
        if verified_payment != None:
            verified_payment = True
        else:
            verified_payment = False

        #may or may not be present
        promotion_tags = job.find('div', attrs = {'class' : 'JobSearchCard-primary-promotion'})
        promotions = []
        if promotion_tags != None:
            promotion_tags = promotion_tags.find_all('span')
            for promotion in promotion_tags:
                promotion_text = promotion.text
                promotions.append(promotion_text)

        contest = job.find('svg', attrs = {'class' : 'flicon-trophy'})
        if contest != None:
            contest = True
        else:
            contest = False


        #put all the info for one job in a list
        job_info = [job_title, description, url, tags,  price, avg_bid, bids, days_remaining, verified_payment, promotions, contest]
        job_list.append(job_info)

#-----------------------------------------------------------------------------

#save data to csv

with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(job_list)