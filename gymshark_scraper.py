import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

# Mens page : https://us.shop.gymshark.com/collections/all-products/mens
# Womens page : https://us.shop.gymshark.com/collections/all-products/womens
# Accessories page : https://us.shop.gymshark.com/collections/accessories

def getData(url):
    # Requests to website
    req = requests.get(url)
    # Beautiful Soup Instated 
    soup = BeautifulSoup(req.text, "html5lib")

    return soup 
        
def parseData(soup):

    # Books found stored in an array as [{title, rating, price, availability, link}]
    products = []

    # List of Products located in div
    listOfProducts = soup.find('div', class_ ='product-grid_grid__UbelU')

    #List of books are stored in an article class tag
    articles = listOfProducts.find_all('article', class_='product-card_product-card__gB8_b')

    for article in articles:
        # Get titles
        link = article.find('a')
        productName = link['title']

        # Get link
        link = link['href']

        # Get color
        color = article.find('p', class_ = 'product-card_product-colour__JApvJ')
        color = color.text

        # If there is a sale going on 

        # Get Price
        price = article.find('span', class_ = 'product-card_product-price__bNBmg')
        price = price.text
        price = float(price[1:])

        # Get Sale Price
        # preSalePrice = article.find('span', class_ = 'product-card_compare-at-price__2MQSu')
        preSalePrice = None
        if article.find('span', class_ = 'product-card_compare-at-price__2MQSu'):
            preSaleCheck = article.find('span', class_ = 'product-card_compare-at-price__2MQSu')
            preSalePrice = preSaleCheck.text
            preSalePrice = float(preSalePrice[1:])
        
        #Append each book info item from dictionary into books list 
        products.append([productName, color, price, preSalePrice,link])

    return products

def getnumProducts(soup):
    
    numProducts = soup.find('span', class_='product-filters_count__fk56Z')
    numProducts = numProducts.text
    numProducts = int(numProducts.split()[0])

    return numProducts

def main():
    # Time taken to scrape site for objects
    # Start Time
    start = time.time()

    # Base url
    # base_url = 'https://us.shop.gymshark.com/collections/joggers-sweatpants/mens'
    base_url = sys.argv[1] #Argument after name of python file 

    # Gets total number of products from first page 
    data = getData(base_url)
    numProducts = getnumProducts(data)

    # Form new url to view all products 
    new_url = base_url + f'?viewAll={numProducts}'

    # Retrieves page with all product data
    time.sleep(20)
    allProductsData = getData(new_url)

    # Parses data 
    allProducts = parseData(allProductsData)

    # Convert to pandas dataframe
    df = pd.DataFrame(allProducts, columns=['name', 'color', 'price', 'preSalePrice','link'])
    
    # Convert to csv file
    file_name = sys.argv[2]
    df.to_csv(file_name, index = False)

    # End time
    end = time.time()
    print('Execution Time: ', (end - start), 'seconds')
    print('Items Collected:', len(df))

main()

# python3 gymshark_scraper.py https://us.shop.gymshark.com/collections/all-products/mens gymshark_mens.csv










