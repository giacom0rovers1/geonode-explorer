#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 18:52:38 2023

@author: giacom0rovers1
"""

import requests
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime


def GET_loop(url, flt, types):
    print(">> Getting online resources...")
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
    # owner = []
    # count = []
    
    err = False
    
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
                last = data["page_size"] if x < 0 else data["page_size"] - x
                
                for id in range(0, last):
                    
                    # select one resource
                    res = data["resources"][id]
                    
                    pk.append(res.get("pk"))                        # identifier
                    uuid.append(res.get("uuid"))                    # uuid
                    title.append(res.get("title"))                  # title
                    rtype.append(res.get("resource_type"))          # data type
                    lic.append(res["license"].get("identifier"))    # license
                    cdate.append(res.get("created"))                # creation date
                    ldate.append(res.get("last_updated"))           # last updated date
                    abst.append(res.get("abstract"))                # abstract
                    alt.append(res.get("alternate"))                # alternate text
                    doi.append(res.get("doi"))                      # Digital Object Identifier

                    # author: "username (full name)"
                    name_fields = ["owner", "metadata_author", "poc"]
                    str = []
                    for field in name_fields:
                        str.append(res[field].get("username") + " (" +
                                   res[field].get("first_name") + " " + 
                                   res[field].get("last_name") + ")")
                    if not str[0] == str[1] == str[2]:
                        warnings.warn("Warning: more than one person involved...")
                    author.append(str[0]) # select owner only (first entry)
                    
                    # > For loop ends here._
            else:
                print(url)
                print(f">> Error: {response.status_code}")
                err = True
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
        
    if err == True:
        raise ConnectionError("Something went wrong.")
    else:
        print(">> Done.")
        return df




class content:
    '''
    Metadata container for GeoNode archives
    '''

    def __init__(self, name, nickname, url):
        
        # Inputs
        self.name = name
        self.nick = nickname
        self.url = url
        
        # Fixed query parameters
        self.flt   = '?filter{resource_type}='
        self.types = ('dataset', 'map', 'document', 'geostory', 'dashboard')

        # Rest API calls
        self.dt = datetime.now()
        self.df = GET_loop(self.url, self.flt, self.types)
        
        # Ancillary variables
        self.Authors = list(set(self.df["Author"]))
        self.sorted_df  = self.df.sort_values("Created")        
        self.sorted_df2 = self.df.sort_values("Last updated")
        self.idx  = self.sorted_df.sort_index(ascending = True).index
        self.idx2 = self.sorted_df2.sort_index(ascending = True).index
        
        self.nR = len(self.df)
        self.nA = len(self.Authors)
        
    # Table functions
    
    def summary(self):
        print(f"Resources:\t\t{self.nR}")
        print(f"Authors:  \t\t{self.nA}")
        print("\nComposition:")
        for i in range(0, len(self.types)):
            print(f"\t\t\t\t{len(np.where(self.df.Type==self.types[i])[0])} \t {self.types[i]}s")
        print(f"\nFirst upload: \t{np.min(self.df['Created']).strftime('%Y/%m/%d %H:%M:%S')} UTC")
        print(f"Last edit:    \t{np.max(self.df['Last updated']).strftime('%Y/%m/%d %H:%M:%S')} UTC")
        
    
    def print_DF(self):
        print(f"{self.name} contents at {self.dt.strftime('%Y/%m/%d %H:%M:%S')} UTC:")
        print(self.df)
        
    def save_CSV(self):
        self.df.to_csv(self.nick + f"_table_{self.dt.date()}.csv")
        

    # Exploratory graphs

    def plot_AuthorsHist(self, save=False):
        self.fig01 = plt.figure(figsize=(6.4, 4.8), dpi=300)
        self.fig01.suptitle("Authors", fontsize=16)
        self.fig01.text(0.5, 0.9, f"[url request at {self.dt.strftime('%Y/%m/%d %H:%M:%S UTC')}]", 
                   horizontalalignment="center", color="grey")
        
        ax = self.df["Author"].value_counts().plot(kind='bar', 
                                         ylabel='Resources count')
        ax.bar_label(ax.containers[0], label_type='edge')
        plt.tight_layout()
        
        if save:
            self.fig01.savefig(self.nick + '_authors.png')
        
    def plot_TypesPie(self, save=False):
        self.fig02 = plt.figure(figsize=(6.4, 4.8), dpi=300)
        self.fig02.suptitle("Resource types", fontsize=16)
        self.fig02.text(0.5, 0.9, f"[url request at {self.dt.strftime('%Y/%m/%d %H:%M:%S UTC')}]", 
                   horizontalalignment="center", color="grey")
        
        self.df["Type"].value_counts().plot(kind='pie', 
                                       autopct='%1.1f%%')
        plt.tight_layout()
        
        if save: 
            self.fig02.savefig(self.nick + '_restype.png')

    def plot_AggregTS(self, save=False):
        self.fig03 = plt.figure(figsize=(6.4, 4.8), dpi=300)
        self.fig03.suptitle("Aggregated upload history", fontsize=16)
        self.fig03.text(0.5, 0.9, f"[url request at {self.dt.strftime('%Y/%m/%d %H:%M:%S UTC')}]", 
                   horizontalalignment="center", color="grey")
        
        plt.plot(self.sorted_df["Created"], self.idx, label="Created")
        plt.plot(self.sorted_df2["Last updated"], self.idx2, label="Last updated")
        
        plt.xticks(rotation=90)
        plt.legend()
        plt.ylabel("Resources count")
        plt.xlabel("Time (UTC)")
        plt.tight_layout()
        
        if save:
            self.fig03.savefig(self.nick + '_population.png')
            
        
    def plot_Contributions(self, save=False):
        self.fig04=plt.figure(figsize=(6.4, 4.8), dpi=300)
        self.fig04.suptitle("Contribution history per author", fontsize=16)
        self.fig04.text(0.5, 0.9, f"[url request at {self.dt.strftime('%Y/%m/%d %H:%M:%S UTC')}]", horizontalalignment="center", color="grey")
        
        plt.scatter(self.sorted_df["Created"], self.sorted_df["Author"], label="Created")
        plt.scatter(self.sorted_df["Last updated"], self.sorted_df["Author"], label="Last updated")
        
        plt.xticks(rotation=90)
        plt.legend()
        plt.ylabel("Author")
        plt.xlabel("Time (UTC)")
        plt.tight_layout()
                
        if save:
            self.fig04.savefig(self.nick + '_activity.png')

            
    ## TODO
    
    # def load_previous()
        # scans for CSVs and loads them as content (?) objects (missing infos) 
        
    # def track_changes()
        # shows changes since last CSV save (both in summary-like form and with figures)
        # timeline plot could show points/lines corresponding to the different CSVs stored locally
        
    
    