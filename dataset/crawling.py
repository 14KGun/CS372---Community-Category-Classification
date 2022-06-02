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

# import packages and modules
from urllib import request
from bs4 import BeautifulSoup

# function ~~
def f(category):
    url = baseUrl + category + searchOption
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('div._1oQyIsiPHYt6nx7VOmd1sz')
    print(len(elements))
f(categories[0])

# entire process
for category in categories:
    print(category)
