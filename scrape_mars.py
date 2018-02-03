# MongoDB and Flask Application

# Dependencies
from bs4 import BeautifulSoup
from splinter.exceptions import ElementDoesNotExist
from splinter import Browser
import requests
import pymongo
import re
import pandas as pd

def scrape():

    # define the empty dictionary to store data
    
    scrape_data = []

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # results are returned as an iterable list
    results = soup.find_all('', class_="slide")

    mars_news_main = []

    for result in results:
    
        mars_news = {}
        
        # Identify and return title of news
        news_title = result.find("div", class_="content_title").text
        # Identify and return paragraph text
        news_p = result.find("div", class_="rollover_description_inner").text

        mars_news["news_title"] = news_title

        mars_news["news_text"] = news_p

        # append new info to the master dictionary (index 0)

        mars_news_main.append(mars_news)

        # Print results only if title, price, and link are available
        #print(result)
        print("-----------------------------------")
        print(news_title)
        print(news_p)

    scrape_data.append(mars_news_main)

    #JPL Mars Space Images - Featured Image

    mars_image_dict = {}

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser = Browser('chrome', executable_path='chromedriver', headless=False)

    browser.visit(url)

    mars_html = browser.html
    mars_soup = BeautifulSoup(mars_html, 'html.parser')

    # Obtain the URL of the main image

    article = mars_soup.find("article")
    article_path = article.get("style")
    value = re.search("'(.+?)'", article_path)
    featured_image = value.group(1)
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image
    mars_image_dict["main_image"] = featured_image_url

    # index 1

    scrape_data.append(mars_image_dict)

    # MARS Weather

    mars_weather_dict = {}

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page using Splinter
    browser = Browser('chrome', executable_path='chromedriver', headless=False)

    browser.visit(url)

    mars_twitter_html = browser.html
    mars_twitter_soup = BeautifulSoup(mars_twitter_html, 'html.parser')

    article_tweets = mars_twitter_soup.find_all("p", class_="TweetTextSize")
    article_tweets
    sol_text = "Sol "

    for tweet in article_tweets:
        print(tweet)
        if sol_text in tweet.text:
            latest_tweet = tweet.text
            break

    print("-------------------------------")        
    print(latest_tweet)

    mars_weather_dict["latest_tweet"] = latest_tweet

    # index 2

    scrape_data.append(mars_weather_dict)

    # URL of Mars Facts

    table_data = {}

    url = 'https://space-facts.com/mars/'

    # Read the html data and convert to a list

    tables = pd.read_html(url)
    table_data["Mars_Data"] = tables

    #index 3

    scrape_data.append(table_data)

    # Mars Hemispheres

    browser = Browser('chrome', headless=False)
    base_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(base_url)
    hem_html = browser.html
    hem_soup = BeautifulSoup(hem_html, 'html.parser')

    hem_links = hem_soup.find("div", class_="collapsible results")

    hem_images = hem_links.find_all("div", class_="item")
    hem_images
    root_url = "https://astrogeology.usgs.gov"

    # store data in this list of dictionaries
    hemisphere_image_urls = []

    # loop through all he hemisphere images
    for result in hem_images:
        
        # stoe the image link
        image_link = result.find("a", class_="itemLink").get("href")
        final_image_link = root_url + image_link
        print(final_image_link)
        browser.visit(final_image_link)

        hem_dict = {}
        page_html = browser.html
        soup = BeautifulSoup(page_html, 'html.parser')
            
        article = soup.find("img", class_="wide-image").get("src")
        feature_url = root_url + article
        site_title = soup.find("title").text
        value = re.search("(.+?)Enhanced", site_title)
        htitle = value.group(1)
        print("Feature URL: " + feature_url)
        print("Title: " + htitle)
        hem_dict["title"] = htitle
        hem_dict["img_url"] = feature_url
        
        hemisphere_image_urls.append(hem_dict)
            
    hemisphere_image_urls  

    # index 4

    scrape_data.append(hemisphere_image_urls)

    print(scrape_data) 
    return scrape_data

# sample_data = scrape()
# print(sample_data)