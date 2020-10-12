from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

mars_import = {}

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find("div", class_="bottom_gradient").text
    news_p= soup.find("div", class_="article_teaser_body").text

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    html = browser.html

    time.sleep(1)

    soup = BeautifulSoup(html, 'html.parser')
    image_url = soup.find("article", class_="carousel_item")["style"]
    clean=image_url.strip("background-image: url('")
    clean=clean.strip("');")
    featured_image_url="https://www.jpl.nasa.gov"+clean

    fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)
    df=tables[0]
    df.columns=["Measurement", "Value"]
    mars_table = df.set_index("Measurement")
    mars_table = mars_table.to_html()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_home = 'https://astrogeology.usgs.gov'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []

    find1=soup.find('div', class_='result-list')
    results = find1.find_all("div", class_= "item")

    for result in results:
        name = result.find("h3").text
        #Source: https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
        #Source 2: https://stackoverflow.com/questions/29773368/splinter-how-to-click-a-link-button-implemented-as-a-div-or-span-element
        browser.click_link_by_partial_text("Enhanced")
        new_html=browser.html
        new_soup = BeautifulSoup(new_html, 'html.parser')

        img_link = new_soup.find('img', class_ = 'wide-image')['src']
        image_url = url_home + img_link
    
        hemisphere_image_urls.append({"Title": name, "Link": image_url})
    
    mars_import ={
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_table": mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    # Return results
    return mars_import

if __name__ == "__main__":
    scrape()


