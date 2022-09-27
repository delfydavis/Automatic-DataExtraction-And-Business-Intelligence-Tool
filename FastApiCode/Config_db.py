# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 00:10:41 2022

@author: DELFY DAVIS
"""

from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = "sqlite:///./finaltaskdb.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
meta= MetaData()
conn=engine.connect()

