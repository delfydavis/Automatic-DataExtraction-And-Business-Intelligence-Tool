# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 01:33:32 2022

@author: DELFY DAVIS
"""

from fastapi import FastAPI
from routes_index import user,user1,user3
app= FastAPI()
sub = FastAPI(openapi_prefix='/subapi')
app.include_router(user1,tags=['DATABASE FEATURES'])
sub.include_router(user,prefix='/DataBase',tags=['TABLE LOCATIONS'])
app.mount('/subapi', sub) #mounting subapi for location
#app.include_router(user3,prefix='/DataBase',tags=['TABLE STATIONS'])
sub.include_router(user3,prefix='/DataBase',tags=['TABLE STATIONS'])

#for sub application
#http://127.0.0.1:8000/subapi/docs

#