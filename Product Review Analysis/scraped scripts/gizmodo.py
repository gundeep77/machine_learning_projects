#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

#%%

def findURLs():
    reviewURLs = []
    driver = webdriver.Chrome(executable_path='chromedriver.exe')

    for i in range(0,100,20):
        driver.get('https://gizmodo.com/reviews/smartphones?startIndex=%d'%i)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article', {'class':'js_post_item'})
        for article in articles:
            link = article.find('a', {'class':'sc-1out364-0 hMndXN js_link'})['href']
            reviewURLs.append(link)

    driver.close()
    return reviewURLs

def getReview(urls):
    reviews = []
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    for url in urls:
        reviewContent = ''
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        contentElement = soup.find('div', {'class':'js_post-content'})
        p_all = contentElement.find_all('p', {'class': 'sc-77igqf-0 bOfvBY'})
        for p in p_all:
            reviewContent += p.text
        reviews.append(reviewContent)
    return reviews
#%%
urls = findURLs()
reviews = getReview(urls)
reviewsDf = pd.DataFrame({'URL': urls, 'Review': reviews})
reviewsDf.head()
reviewsDf.to_csv('CSV/gizmodo.csv')
# %%
