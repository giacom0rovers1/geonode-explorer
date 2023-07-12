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

# Comment: The more away the two curves are from each other, the more active and maintained the archive is. 
# The SIP started to be populated in late June 2022 and has seen two major periods of upload activities in September 2022 and March 2023. Activity has resumed in June 2023 and it is ongoing.
