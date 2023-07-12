#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:40:10 2023

@author: giacom0rovers1
"""

import geonodexplorer as geo

sip = geo.content(name     = "SCORE EU Platform", 
                  nickname = "SIP", 
                  url      = "https://platform.score-eu-project.eu/api/v2/resources")
                  
sip.print_DF()

sip.summary()

sip.save_CSV()

sip.plot_AuthorsHist(True)
sip.plot_TypesPie(True)
sip.plot_AggregTS(True)
sip.plot_Contributions(True)