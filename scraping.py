
#Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    #Initiate headless driver for deployment/Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    #Stop webdriver/browser and return data
    browser.quit()
    return data

#Scrape Mars news
def mars_news(browser):

    #Visit the Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    #Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text',wait_time =1)

    #Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

   #try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
    
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div',class_='content_title').get_text()


        #Use the parent element to find the paragraph text
        news_p = slide_elem.find('div',class_ = 'article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# Scrape JPL Space Images Featured Image
def featured_image(browser):

     # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html,'html.parser')

    #Add try/except for error handling
    try:

        #Find the relative image url (the one that won't chaimgnge when this is no longer the first image on the page)
        img_url_rel = img_soup.find('img',class_ = 'fancybox-image').get('src')
        img_url_rel

    except AttributeError:
        return None
        
    #Use the base url to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# Scrape Mars Facts
def mars_facts():

    #add try/except for error handling
    try:

    #use read_html to scrape the facts tables into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    #  Assign columns and set index of Dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #Convert table back to html, add bootstrap
    return df.to_html()

def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.



    #parse main page 
    html = browser.html
    mainpg_soup = soup(html,'html.parser')
    #print(mainpg_soup.prettify())



    #find tags for links to four sub pages with images
    div_items = mainpg_soup.find_all('div',class_='item')
    len(div_items)

    #for loop to go through all four images
    #loop through all 4 sub pages, capturing image links and titles
    for item in div_items:
        
        #get the relative url of the sub page with the hemisphere image
        link = item.find('a')['href']
        
        #construct the whole/absolute url
        absolute_url = url+link
        
        #grab the title of the link
        title = item.find('h3').text
        
        #go visit the sub page
        browser.visit(absolute_url)
        
        #parse sub page
        html_sub=browser.html
        
        #convert sub page to a beautiful soup
        sub_soup=soup(html_sub,'html.parser')
        
        #find and capture the url for the jpg image
        hemi_img = sub_soup.find('li').find('a')['href']
        
        #convert image relative url to absolute url
        hemi_img_abs_url = url+hemi_img
        
        #append to list of dictionaries of hemisphere image urls and titles
        hemisphere_image_urls.append({"img_url":hemi_img_abs_url,"title":title})

    return hemisphere_image_urls



if __name__ == "__main__":
    #If running as script, print scraped data
    print(scrape_all())


