from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from flask import Flask


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser ('chrome', **executable_path, headless = False)
    title,paragraph = news(browser)

    mars={
        "title":title,
        "paragraph": paragraph,
        'image': featured_image_url(browser),
        'facts': facts(),
        'hemispheres': hemispheres(browser) 
    }
    return mars

def news(browser):
    url= 'https://mars.nasa.gov/news/'
    browser.visit(url)
    Title=browser.find_by_css('div.content_title a').text
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    Paragraph = soup.find('div',class_='article_teaser_body').text
    return Title,Paragraph


def featured_image_url(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.find_by_css('img.fancybox-image')['src']
    return featured_image_url

def facts():
    return pd.read_html('https://space-facts.com/mars/')[0].to_html()

def hemispheres(browser):
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    links = browser.find_by_css('a.itemLink h3')
    List=[]
    for i in range(len(links)):
        hemisphere = {}
        hemisphere['title']=browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3').click()
        hemisphere['url']=browser.find_by_text('Sample')['href']
        browser.back()
        List.append(hemisphere)
    browser.quit()
    List
    return hemispheres
