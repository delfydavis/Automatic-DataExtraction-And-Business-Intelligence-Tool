# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 00:12:47 2022

@author: DELFY DAVIS
"""

from pydantic import BaseModel
class Location(BaseModel):
    location_id:int
    location_name:str
    population:int
    available_houses:int
    class Config:
        orm_mode = True
        
class Station(BaseModel):
    station_id:int
    name:str
    platforms_count:int
    station_boss:str
    class Config:
        orm_mode = True