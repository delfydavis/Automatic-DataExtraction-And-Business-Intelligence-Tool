# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 00:11:28 2022

@author: DELFY DAVIS
"""

from Config_db import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String

Locations =Table ('locations',meta,Column('location_id',Integer, primary_key=True),
   Column('location_name',String(80)),
   Column('population',Integer),
   Column('available_houses',Integer)
   )

Stations =Table ('stations',meta,Column('station_id',Integer, primary_key=True),
   Column('name',String(80)),
   Column('platforms_count',Integer),
   Column('station_boss',String(80))
   )
