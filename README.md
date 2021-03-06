# Mission-to-Mars
Web scraping module

# Overview
This week we explored web scraping. Read the "How to Make it Work" section to know how to run the project. Below that in the "How it is built" section are details of the individual elements of the project.  Together, these elements create a web page displaying data about Mars which can be updated via a webscrape every time the button "Scrape New Data" is clicked. 

# How to make it work
- Make sure you have opened mongo to run in the background: open a command prompt and type mongod, then open a second command prompt and type mongo
- Make sure you have created the mars_app database in mongo
- Run app.py from the command prompt or through VSCode
- Control + click on the 1270.0.0:5000 link that comes up, a browser window will open with your index.html displayed
- Click on the Scrape New Data button
- Enjoy!

# How it is built
This project combines two python files, scraping.py and app.py, an index.html file, and a mongo database called mars_app. 

## Python scraping.py code
This python code is where the actual scraping happens. This code only defines functions and will not do anything all by itself. Here are the some details about the code:

### Websites
In the file scraping.py we visit the following websites to scrape the following data:
  - https://redplanetscience.com - grab the news story, get the title and the summary/article teaser body
  - https://spaceimages-.com - grab the newest image of Mars
  - https://galaxyfacts-mars.com - grab a table of facts about Mars
  - https://marshemispheres.com/ - grab 4 high resolution images of Mars' hemispheres

### Dependencies
We use the following dependencies:
  - Splinter - to navigate to websites, click buttons, grab the html code
  - ChromeDriverManager - for splinter to use to operate Chrome
  - Beautful soup - to parse through the html code, by creating a soup item, and zeroing in on the elements we want
  - Pandas - to convert the Mars facts table into a dataframe for easier handling of that data
  - Datetime - to capture the time the data was scraped

### Functions 
The following functions are created: 
  - mars_news() - scrapes the Mars news website
  - featured_image() - scrapes the most recent featured image of Mars
  - mars_facts() - scrapes the table of facts about Mars
  - mars_hemispheres() - scrapes 4 high resolution images of Mars' hemispheres
  - scrape_all() - runs all 4 scraping functions and gathers all scraped data into a dictionary which is returned
  
## HTML index.html
This file creates the structure for the end user interface. The initial page is not populated with data, a button is created that triggers the scraping code, and then the page refreshes to display the scraped data. The html and css/bootstrap in the code determine the layout, colors, fonts, and functionality of the page. Double curly brackets {{}} surround data that is being pulled from the mongo database into the web page we are building. A for loop converts the Mars facts into a nice table.

## Python app.py file
This file is really what holds the whole project together.  It uses Flask to create a little server that renders our index.html file in the browser. It imports the scraping.py file for access to the functions there. It creates two routes, one for the home page of the html and one to activate the scraping.py code by calling the scrape_all() function. It also creates a connection to a mongo database, and stores the scraped data in there after it is retrieved, for it to be retrieved in turn inside the index.html code. 

## Mongo DB
Before the scraping can be run, a database called mars_app must be created inside Mongo. App.py opens the connection to mongo, and stores the data there. The html draws the data through app.py into the refreshed web page which contains all thte data.

