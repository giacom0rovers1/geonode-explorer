#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 18:12:07 2023

@author: giacom0rovers1
"""
# import os
import requests
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# empty lists
pk = []
uuid = []
title = []
author = []
rtype = []
lic = []
cdate = []
ldate = []
abst = []
alt = []
doi = []


# TODO: cross check con le categorie di geonode (api/v2/categories)

url = "https://platform.score-eu-project.eu/api/v2/resources"

# params = {"Authorization" : "Bearer UjYxYUKtEoDg3ifrucJNnMEr8djazr", "format" : "json"}
# page = 1
# page_size = 10
# total = 132

while url != None:
    response = requests.get(url)
    
    if response.status_code == 200:     
    
        # GET data
        data = response.json()
        
        print(f"Page {data.get('page')}  [page size: {data.get('page_size')}, total: {data.get('total')}]")
    
        # next page
        url = data["links"].get("next")
        
    
        for id in range(0, data["page_size"]-1):
            
            # select one resource
            res = data["resources"][id]
            
            # identifier
            pk.append(res.get("pk"))
            
            # uuid
            uuid.append(res.get("uuid"))
            
            # title
            title.append(res.get("title"))
            
               
            # author [username (full name)]
            name_fields = ["owner", "metadata_author", "poc"]
            str = []
            for field in name_fields:
                str.append(res[field].get("username") + " (" +
                           res[field].get("first_name") + " " + 
                           res[field].get("last_name") + ")")
            if not str[0] == str[1] == str[2]:
                warnings.warn("Warning: more than one person involved...")
            author.append(str[0]) # select owner only (first entry)
            
            # data type
            rtype.append(res.get("resource_type"))
            
            # license
            lic.append(res["license"].get("identifier"))
            
            
            # creation date
            cdate.append(res.get("created"))
            
            # last updated date
            ldate.append(res.get("last_updated"))
            
            # abstract
            abst.append(res.get("abstract"))
            
            # alternate text
            alt.append(res.get("alternate"))    
            
            # Digital Object Identifier
            doi.append(res.get("doi"))    
            
            # > For loop ends here._
    else:
        print(url)
        print(f"Error: {response.status_code}")
        break
    
    # > While loop ends here._


d = {"PK" :             pk,
     "UUID" :           uuid,
     "Title" :          title,
     "Author" :         author, 
     "Type" :           rtype, 
     "License" :        lic,
     "Created" :        cdate,
     "Last updated" :   ldate,
     "Abstract" :       abst,
     "Alt-name" :       alt,
     "DOI" :            doi}

df = pd.DataFrame(data=d)

# Dates as dates
for key in ["Created", "Last updated"]:
    df[key] = df[key].astype("datetime64[ns]")

# Categorical
for key in ["Author", "Type", "License"]:
    df[key] = df[key].astype("category")

print(df)
df.to_csv('SIP_table.csv')


len(set(df["Author"]))


# Exploratory graphs

df["Author"].value_counts().plot(kind='bar', ylabel='Count')
df["Author"].value_counts().plot(kind='pie', autopct='%1.1f%%') #, explode = (0.1, 0, 0, 0, 0, 0, 0, 0)


df["Type"].value_counts().plot(kind='pie', autopct='%1.1f%%') # , explode = (0, 0, 0.1, 0)

df["License"].value_counts().plot(kind='bar')

# df["DOI"].value_counts().plot(kind='bar') # DOIs are missing



# Spunti...
# https://medium.com/@kvnamipara/a-better-visualisation-of-pie-charts-by-matplotlib-935b7667d77f

# # Authors
# fig01, ax01 = plt.subplots()
# ax01.hist(df["Author"])
# plt.show()



# Time serie of creation dates (increase number of resources..)
# df.sort_values("Created")["Created"].plot()
# df.sort_values("Last updated")["Last updated"].plot()


sorted_df = df.sort_values("Created")
idx = sorted_df.sort_index(False).index
pp = idx/(len(idx)+1)

sorted_df2 = df.sort_values("Last updated")
idx2 = sorted_df2.sort_index(False).index
pp2 = idx2/(len(idx2)+1)


plt.plot(sorted_df["Created"], pp*100)
plt.plot(sorted_df2["Last updated"], pp2*100)
plt.xticks(rotation=90)

plt.legend(["Created", "Last updated"])





# df.groupby(df["Created"].dt.month).count().plot(kind="bar")



# > Completed._



# Drafts

# keys = ["first_name", "last_name"] #, "username"]
# [data["resources"][0]["owner"].get(key) for key in keys]

# data["resources"][0]["owner"].items()


