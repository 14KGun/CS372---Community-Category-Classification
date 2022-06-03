"""
KAIST CS372 - Classification of online post categories based on community tendencies
- 20190052 Geon Kim, 20190703 Geonha Hwang
- 2022.06.02 / crawling.py
- Crawl sites by category and save them as a csv file to create a dataset
"""

# config parameter
baseUrl = "https://www.reddit.com/r/"
categories = ["entertainment", "politics", "travel", "parenting", "business", "sports"]
searchOption = "/top/?t=year" # most popular articles of the year
postPerCatecory = 1000 # the number of posts collected per category

# import packages and modules
import time
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver

# function to get posts from html
def html2posts(html):
    posts = []
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('div._1oQyIsiPHYt6nx7VOmd1sz')
    for element in elements:
        # dont push empty element
        if len(element.select('h3._eYtD2XCVieq6emjKBH3m')) < 1: continue 
        # dont push advertisement
        if len(element.select('span._2oEYZXchPfHwcf9mTMGMg8')) > 0: continue
        
        title = element.select('h3._eYtD2XCVieq6emjKBH3m')[0].get_text()
        content = ' '.join([row.get_text() for row in element.select('p._1qeIAgB0cPwnLhDF9XSiJM')])
        image = (len(element.select('img._1dwExqTGJH2jnA-MYGkEL-')) + len(element.select('img._2_tDEnGMLxpM6uOa2kaDB3'))) > 0
        video = len(element.select('._3UEq__yL-82zX4EyuluREz')) > 0
        link = element.select('a._13svhQIUZqD9PVzFcLwOKT')
        link = link[0]['href'] if len(link) > 0 else ''
        posts.append([title, content, link, image, video, category])
    return posts

# function to save as a csv file
def saveAsCsv(data, filename):
    df = pd.DataFrame(data, columns=['title', 'content', 'link', 'image', 'video', 'category'])
    df.to_csv(filename, index=True, encoding='utf-8')

# function to get all posts for category
def getPostsFromCategory(category):
    # load chrome web driver
    url = baseUrl + category + searchOption
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    # crawling with scrolling
    posts = []
    targetHeight = 0
    while len(posts) < postPerCatecory:
        screenHeight = driver.execute_script("return window.screen.height;")
        targetHeight += screenHeight
        driver.execute_script("window.scrollTo(0, {x});".format(x=targetHeight))
        while driver.execute_script("return document.body.scrollHeight;") < targetHeight:
            driver.execute_script("window.scrollTo(0, {x});".format(x=targetHeight))
            time.sleep(0.2)
        posts = html2posts(driver.page_source)
        if len(posts) > 980: saveAsCsv(posts, 'dataset-reddit-'+category+'.csv')
        print(len(posts))
    return posts[:postPerCatecory]

# entire process
if __name__ == "__main__":
    for category in categories[4:]:
        posts = getPostsFromCategory(category)
        saveAsCsv(posts, 'dataset-reddit-'+category+'.csv')
