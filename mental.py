import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class gloscience:
    def __init__(self):
        self.Description = []
        self.hreflevels = []
        self.productnames = []
        self.producturls = []
        self.productdescriptions = []
        self.productqty = []
        self.sku = []
        self.empty = []
        self.productimages =[]


    def getpageUrl(self):
        r = requests.get('https://www.mwdental.com/')
        soup = BeautifulSoup(r.content, 'html.parser')
        level1 = soup.find_all('a', class_="level1")
        print("first function done")
        for link1 in level1:
            print(link1.get('href'))
            self.hreflevels.append(link1.get('href'))
        print("check list")   
        print(self.hreflevels)
        return self.hreflevels
    
    def dataofproduct(self):
        self.getpageUrl()
        for link in self.hreflevels:
            print(link)
            requeststestlink = requests.get(link)
            souptest = BeautifulSoup(requeststestlink.content, 'html.parser')
            productname = souptest.find_all('div', class_="product-shop-info")
            for j in productname:
                self.productnames.append(j.find('h5').text)
                self.producturls.append(j.find('a').get('href'))
                self.sku.append("mwdental")
                self.empty.append(" ")
                self.productqty.append("1")
                try:
                    descriptiondata = j.find('div', class_="product-description")
                    self.productdescriptions.append(descriptiondata.text)
                except:
                    self.productdescriptions.append(descriptiondata)
        
            productimage = souptest.find_all('div', class_="product-image")
            for i in productimage:
                self.productimages.append(i.find('img').get('src'))
       
        print(len(self.productimages))
        print(len(self.productnames))
        print(len(self.productdescriptions))
        
        technologies= {
            "Seller Platform": self.sku,
            "Seller SKU" :self.empty,
            "Manufacturer Name":self.sku,
            'Manufacturer Code':self.empty,
            'Product Title':self.productnames,
            'Description' : self.productdescriptions,
            "Packaging":self.empty,
            'QTY':self.productqty,
            "Catagory" : self.empty, 
            "Subcategory" : self.empty,
            "Product Page URL" : self.producturls, 
            "Attachment URL" : self.empty,
            "Images URL" : self.productimages
    
            }
        df = pd.DataFrame(technologies)
        df.to_csv("mdentalmain.csv",index=False)
        return df




if __name__ == "__main__":
    SPlatfrom = "Glo Science Solutions"
    scraper = gloscience()
    scraped = scraper.dataofproduct()
    time.sleep(5)