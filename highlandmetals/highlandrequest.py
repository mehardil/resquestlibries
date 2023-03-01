import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

class Highlandrequest:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
        }
       
        self.url = url

        self.productnamedata = []
        self.producturls = []
        self.productdescriptiondata = []
        self.productqtydata = []
        self.productpackagedata = []
        self.productsku = []
        self.empty = []
        self.productimagedata =[]
        self.platform = []
       


    def getpageUrl(self):
        for key in range(0,38):
            print(url+'?p=SearchBody&search=&pg='  + str(key))
            page = requests.get(url+'?p=SearchBody&search=&pg='  + str(key), headers=self.headers)
            print(page.status_code)
            soup = BeautifulSoup(page.content, 'html.parser')
            urlofeachproduct = soup.find_all('a', class_="preview")
            for link in urlofeachproduct:
                print(link.get('href'))
                self.producturls.append(link.get('href'))
            print("check list")   
            print(self.producturls)
            print(len(self.producturls))
        return self.producturls


    def dataofproduct(self):
        self.getpageUrl()
        j = 0 
        for pageproduct in self.producturls:
            j = j+1
            print(j)
            print(pageproduct)
            requeststestlink = requests.get(pageproduct)
            souppages = BeautifulSoup(requeststestlink.content, 'html.parser')
            
            ####title ###packaging ####quntity
            try:
                productname = souppages.select('h1.margin-bottom-mini span#labelDescription')
                print(productname[0].text)
                self.productnamedata.append(productname[0].text)
                package =  re.findall(r'\b[a-zA-Z]+\b', productname[0].text)[-1]
                print(package)
                qty = re.findall(r'\d+(?!\d)', productname[0].text)[-1]
                print(qty)
                if package == "wires":
                    package = "pack"
                if package == "BASE":
                    package = " "
                    qty = " "
                if package == "spool":
                    package = " "
                if package == "spools":
                    package = "pack"
                print(qty)
                if package == 'of':
                    package = "pack"
                print(package)
                if package =='A':
                    package = "PK"
                if package == "ties":
                    package = "pack"
                    qty = "10"
                if package == "DO":
                    package = 'PK'
                if package == "springs":
                    package = " "
                if package == "packs":
                    package = "pack"
                self.productpackagedata.append(package)
                self.productqtydata.append(qty)
            except:
                self.productnamedata.append("none")
                self.productpackagedata.append("none")
                self.productqtydata.append("none")
            
            ##sku ## empty data  ## platform
            try:
                productid = souppages.find('span', class_="itemid label label-primary")
                self.productsku.append(productid.text[6:])
                self.empty.append(" ")
                print(productid.text[6:])
                self.platform.append("highlandmetals")
            except:
                self.productsku.append("none")
                self.empty.append(" ")
                self.platform.append("highlandmetals")
            
            
            
            ###image
            try:
                productimage = souppages.select_one('a#_ctl0__ctl4__ctl1_hyperlinkCurrentView img')
                self.productimagedata.append(productimage.get('src'))
                
            except:
                self.productimagedata.append("none")
            
             ####description
            try:
                productdescription = souppages.select_one('div.padding-left-right-none >div.col-md-7')
                text_content = productdescription.get_text(strip=True, separator=' ')
                print(text_content)
                self.productdescriptiondata.append(text_content[9:])
                
            except:
                self.productdescriptiondata.append("none")
            
        print(len(self.productnamedata))
        print(len(self.productsku))
        print(len(self.productdescriptiondata))
        print(len(self.productimagedata))
        print(len(self.empty))
        print(len(self.productpackagedata))
        print(len(self.productqtydata))
        print("image data")
        print(self.productimagedata)


        technologies= {
            "Seller Platform": self.platform,
            "Seller SKU" :self.productsku,
            "Manufacturer Name":self.platform,
            'Manufacturer Code':self.productsku,
            'Product Title':self.productnamedata,
            'Description' : self.productdescriptiondata,
            "Packaging":self.productpackagedata,
            'QTY':self.productqtydata,
            "Catagory" : self.empty, 
            "Subcategory" : self.empty,
            "Product Page URL" : self.producturls, 
            "Attachment URL" : self.empty,
            "Images URL" : self.productimagedata
    
            }
        df = pd.DataFrame(technologies)
        df.to_csv("dental-highland.csv",index=False)
        return df




if __name__ == "__main__":
    url = 'https://www.highlandmetals.com/store/Main.aspx'
    scraper = Highlandrequest()
    scraped = scraper.dataofproduct()
    time.sleep(5)