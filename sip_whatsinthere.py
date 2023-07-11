#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 18:12:07 2023

@author: giacom0rovers1
"""
# import os
import requests
import warnings
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


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
owner = []
count = []


# datetime object containing current date and time
now = datetime.now()
now_str = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
print("date and time =", now_str)

url   = "https://platform.score-eu-project.eu/api/v2/resources"
flt   = '?filter{resource_type}='

types = ('dataset', 'map', 'document', 'geostory', 'dashboard')

for par in types:
    query = url + flt + par
    print(query)
    
    while query != None:
        response = requests.get(query)
        
        if response.status_code == 200:     
        
            # GET data
            data = response.json()
            
            print(f"Page {data.get('page')}  [page size: {data.get('page_size')}, total: {data.get('total')}]")
        
            # next page
            query = data["links"].get("next")
            
            
            x = data["page"]*data["page_size"] - data["total"]
            
            if x < 0:
                last = data["page_size"] 
            else:
                last = data["page_size"]- x
            
            print(last)
            for id in range(0, last):
                
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

fig01 = plt.figure(figsize=(6.4, 4.8), dpi=300)
fig01.suptitle("Authors", fontsize=16)
fig01.text(0.5, 0.9, f'[url request at {now_str}]', horizontalalignment="center", color="grey")
ax = df["Author"].value_counts().plot(kind='bar', 
                                 ylabel='Resources count')
ax.bar_label(ax.containers[0], label_type='edge')
plt.tight_layout()
fig01.savefig('authors.png')
fig01.show()

fig02 = plt.figure(figsize=(6.4, 4.8), dpi=300)
fig02.suptitle("Categories", fontsize=16)
fig02.text(0.5, 0.9, f'[url request at {now_str}]', horizontalalignment="center", color="grey")
df["Type"].value_counts().plot(kind='pie', 
                               autopct='%1.1f%%')
plt.tight_layout()
fig02.savefig('categories.png')
fig02.show()


# df["License"].value_counts().plot(kind='pie', autopct='%1.1f%%') # no license information
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
idx = sorted_df.sort_index(ascending = True).index

sorted_df2 = df.sort_values("Last updated")
idx2 = sorted_df2.sort_index(ascending = True).index

fig03 = plt.figure(figsize=(6.4, 4.8), dpi=300)
fig03.suptitle("Aggregated upload history", fontsize=16)
fig03.text(0.5, 0.9, f'[url request at {now_str}]', horizontalalignment="center", color="grey")
plt.plot(sorted_df["Created"], idx, label="Created")
plt.plot(sorted_df2["Last updated"], idx2, label="Last updated")
plt.xticks(rotation=90)
plt.legend()
plt.ylabel("Resources count")
plt.xlabel("Time (UTC)")
plt.tight_layout()
fig03.savefig('population.png')
fig03.show()


fig04=plt.figure(figsize=(6.4, 4.8), dpi=300)
fig04.suptitle("Contribution history per author", fontsize=16)
fig04.text(0.5, 0.9, f'[url request at {now_str}]', horizontalalignment="center", color="grey")
plt.scatter(sorted_df["Created"], sorted_df["Author"], label="Created")
plt.scatter(sorted_df["Last updated"], sorted_df["Author"], label="Last updated")
plt.xticks(rotation=90)
plt.legend()
plt.ylabel("Author")
plt.xlabel("Time (UTC)")
plt.tight_layout()
fig04.savefig('activity.png')
fig04.show()




# df.groupby(df["Created"].dt.month).count().plot(kind="bar")



# > Completed._



# Drafts

# keys = ["first_name", "last_name"] #, "username"]
# [data["resources"][0]["owner"].get(key) for key in keys]

# data["resources"][0]["owner"].items()




# url_ows = "https://platform.score-eu-project.eu/api/v2/owners"

# while url_ows != None:
#     response = requests.get(url_ows)
    
#     if response.status_code == 200:     
    
#         # GET data
#         data = response.json()
        
#         print(f"Page {data.get('page')}  [page size: {data.get('page_size')}, total: {data.get('total')}]")
    
#         # next page
#         url_ows = data["links"].get("next")
        
    
#         for id in range(0, data["page_size"]-1):
            
#             # select one resource
#             res = data["owners"][id]
            
#             # identifier
#             pk.append(res.get("pk"))
             
#             # username
#             owner.append(res.get("username") + " (" +
#                          res.get("first_name") + " " + 
#                          res.get("last_name") + ")")
               
#             # count
#             count.append(res.get("count"))
            
#             # > For loop ends here._
#     else:
#         print(url)
#         print(f"Error: {response.status_code}")
#         break
    
#     # > While loop ends here._

# dfo = pd.DataFrame(data={
#     "PK"    : pk,
#     "Owner" : owner,
#     "Count" : count
#     })
