# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 16:48:47 2020

@author: Walden
"""

# import the requests library
import requests
import zipfile
url = 'https://github.com/YancarloOjeda/WTS-2.01/archive/master.zip'

# download the file contents in binary format
r = requests.get(url)

with open("C:\WALDEN\WTS-2.01.zip", "wb") as zip:
    zip.write(r.content)
    

with zipfile.ZipFile('C:\WALDEN\WTS-2.01.zip', 'r') as zip_ref:
    zip_ref.extractall('C:\WALDEN' )