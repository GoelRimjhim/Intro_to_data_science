# IDC409 Project-1  Submitted by- Rimjhim Goel(MS18133) and Chhavi Chahar (MS18136) 
# Group members - MS18133 and MS18136  
# Contribution - MS18133(50%) MS18136(50%)

#********************************************************************#


import requests
# requests - library for making HTTP requests 
from bs4 import BeautifulSoup
#BeautifulSoup - for parsing the data
import pandas as pd
# pandas - to convert the data scraped from the website into a dataframe
from sqlalchemy import create_engine
#sqlalchemy - to push the scraped data to mysql

URL = 'https://www.goodreads.com/list/show/167306.New_horror_for_your_Halloween_reading'
# URL from which data is to be fetched.
p = requests.get(URL)
# requests.get sends HTTP get request to the URL and recieves data
s = BeautifulSoup(p.content, "html.parser")
#passes p as p.content for decoding, the parser used is HTML parser   
books = s.find_all("tr")
#Inspection of the page source tells that the information of each book is stored under tr tag
#find_all fetches information from tr tags from the page. 

bookList = {'Title':[], 'Author':[], 'Average rating and total ratings':[]}
# we create a dictionary to store the relevant information from the HTML.
# We have 3 keys(=3 columns in the database): Title, Author, Average rating and total ratings
for book in books:
    bookList['Title'].append(book.find("span", {"itemprop":"name"}).text)
    bookList['Author'].append(book.find("span", {"itemprop":"author"}).text)
    bookList['Average rating and total ratings'].append(book.find("span", class_ = "minirating").text)
# for each book on the webpage,by inspection, we find the tags under which the title, author and ratings are present
# and append the information in the respective keys 

dataFrame = pd.DataFrame.from_dict(data=bookList)
# create the pandas dataframe from the  bookList dictionary

connection=create_engine("mysql+mysqldb://root:123ds@localhost/mydatabase")
# create an engine to connect the 'mydatabase' database in MySQL to python
dataFrame.to_sql(con=connection, name='goodreads', if_exists='replace', index=False)
# a table named 'goodreads' is created in mydatabase
# the pandas dataframe is pushed to 'goodreads' table
# if_exists = 'replace' replaces data previously present in the table,if any.