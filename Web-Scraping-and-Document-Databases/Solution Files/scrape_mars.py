# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


# In[43]:


#Initialize browser
def init_browser():
# @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


# In[44]:


# Scrape NASA Mars News
def scrape_NASA():
    browser=init_browser()
    
    #visit the NASA Mars News Site](https://mars.nasa.gov/news/
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    #scrape page into soup
    html = browser.html
    soup=BeautifulSoup(html,"html.parser")
    
    #collect the latest News Title and Paragraph Text
    latest_news = soup.find("div", class_="list_text")
    #print(latest_news)
    #news title
    news_title=latest_news.find("div",class_="content_title").text
    #print(news_title)
    #paragraph text
    news_p=latest_news.find("div",class_="article_teaser_body").text
    
    #store in dictionary
    latest_news={
        'title':news_title,
        'paragraph':news_p
    }
    
    return latest_news


# In[45]:


#Scrape JPL Mars Space Images
def scrape_JPL():
    browser = init_browser()
    
    #Visit the url for JPL Featured Space Image 
    #(https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    
    #scrape page into soup
    html=browser.html
    soup=BeautifulSoup(html,"html.parser")
    
    #find and collect the featured image
    featured_image = soup.find("section",class_="centered_text clearfix main_feature primary_media_feature single")                     .find("article").find("a")['data-fancybox-href']
    
    featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image
    
    return featured_image_url


# In[46]:


#scrape Mars Weather
def scrape_mars_weather():
    browser = init_browser()
    #Visit the Mars Weather twitter account [here]
    #(https://twitter.com/marswxreport?lang=en) 
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    
    #scrape page into soup
    html=browser.html
    soup=BeautifulSoup(html,"html.parser")
    
    #scrape the latest Mars weather tweet from the page
    mars_weather=soup.find("div",class_="ProfileTimeline")          .find("div",class_="content").find("p").text
    
    return mars_weather
        


# In[47]:


#scrape Mars Facts
def scrape_mars_facts():
    browser=init_browser()
    
    #Visit the Mars Facts webpage 
    #(http://space-facts.com/mars/) 
    url = 'http://space-facts.com/mars/'
    browser.visit(url)
    
    #scrape page into soup
    html=browser.html
    #soup=BeautifulSoup(html,"html.parser")
    
    #scrape the table containing facts about the planet including Diameter, Mass, etc.
    # use pandas to read the table
    table=pd.read_html(html)
    df =pd.DataFrame(table[0])
    df.columns=['Description','value']
    df=df.set_index('Description')
  
    #Use Pandas to convert the data to a HTML table string
    mars_facts=df.to_html()
    
    return mars_facts


# In[20]:


x=scrape_mars_facts()


# In[54]:


#scrape the images from Mars Hemispheres
def scrape_mars_hemispheres():
    browser=init_browser()
    
    #Visit the USGS Astrogeology site
    #(https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    #scrape page into soup
    html=browser.html
    soup=BeautifulSoup(html,"html.parser")
    
    #find all links to hemisphere image
    all_items=soup.find("div",class_="collapsible results").find_all("div",class_="item")
    
    #initializer hemisphere_image_urls
    hemisphere_image_urls=[]
    
    for item in all_items:

        title=item.find("div",class_="description").find("a").text    
        link='https://astrogeology.usgs.gov' + item.find("a")['href']
        #visit the link and collect in soup
        browser.visit(link)
        soup2 = BeautifulSoup(browser.html,"html.parser")
        img_url=soup2.find("img",class_='wide-image')['src']
        
        dict_item={'title':title,
                  'img_url':'https://astrogeology.usgs.gov'+ img_url}
        
        #add dict to the list
        hemisphere_image_urls.append(dict_item)
    
    return hemisphere_image_urls

