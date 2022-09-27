# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 00:37:31 2022

@author: DELFY DAVIS
"""


from fastapi import APIRouter,Query
from Config_db import conn
from Model_Index import Locations,Stations
from Schema_index import Location,Station
from enum import Enum
import sqlite3
user1 = APIRouter()
user = APIRouter()

user3= APIRouter()
#HomePage
class Tables(str, Enum):
    Location = "Location"
    Station = "Station"
    
 #All  Table from  the DB   
cnx=sqlite3.connect('delfydb.db')
cnx.row_factory = lambda cursor, row: row[0]
cursor=cnx.cursor()
tables=cursor.execute('select name from sqlite_master where type="table"').fetchall()
tables2=[]
for row in tables[1:]:
    tables2.append(row)

#Extract Column Name of Respective table from DB

Column_Name = [[] for i in range(len(tables2))]
for i in range(len(tables2)):
    cursor1=cnx.execute('select * from '+str(tables2[i]))
    Column_Name[i].append(list(map(lambda x: x[0], cursor1.description)))
    
    
@user1.get("/DataBase/{choice}")
async def List_of_Tables(choice: Tables = Query("Tables", choices=tables2, description='List of DB tables')):
    
    if choice=="Location":
        
        return {"Column Names":Column_Name[1]}
        
    elif choice=="Station":
        return {"Column Names":Column_Name[0]}
    

#-------------------------------------------------------------------------------------------------------
#LOCATION
@user.get("/Table/Location")
async def read_data():
    return conn.execute(Locations.select()).fetchall()

@user.post("/Table/Location")
async def write_data(location:Location):
    
    conn.execute(Locations.insert().values(
        location_id=location.location_id,
        location_name=location.location_name,
        population=location.population,
        available_houses=location.available_houses
        ))
    #conn.commit()
    return conn.execute(Locations.select()).fetchall()
@user.get("/Table/Location/{id}")
async def read_data(id:int):
    return conn.execute(Locations.select().where(Locations.c.location_id==id)).fetchall()


@user.put("/Table/Location/{id}")
async def update_data(id:int,location:Location):
    conn.execute(Locations.update().values(
        location_name=location.location_name,
        population=location.population,
        available_houses=location.available_houses
        ).where(Locations.c.location_id==id))
    #conn.commit()
    return conn.execute(Locations.select()).fetchall()

@user.delete("/Table/Location")
async def delete_data(id:int):
    conn.execute(Locations.delete().where(Locations.c.location_id==id))
    #conn.commit()
    return conn.execute(Locations.select()).fetchall()
#--------------------------------------------------------------------------------------------------------
#STATION 
@user3.get("/Table/Station")
async def read_data():
    return conn.execute(Stations.select()).fetchall()
@user3.post("/Table/Station")
async def write_data(station:Station):
    
    conn.execute(Stations.insert().values(
        station_id=station.station_id,
        name=station.name,
        platforms_count=station.platforms_count,
        station_boss=station.station_boss
        
        ))
    #conn.commit()
    return conn.execute(Stations.select()).fetchall()
@user3.get("/Table/Station/{id}")
async def read_data(id:int):
    return conn.execute(Stations.select().where(Stations.c.station_id==id)).fetchall()
@user3.put("/Table/Station/{id}")
async def update_data(id:int,station:Station):
     conn.execute(Stations.insert().values(
         station_id=station.station_id,
         name=station.name,
         platforms_count=station.platforms_count,
         station_boss=station.station_boss
         
         ).where(Stations.c.station_id==id))
     #conn.commit()
     return conn.execute(Stations.select()).fetchall()

@user3.delete("/Table/Station")
async def delete_data(id:int):
    conn.execute(Stations.delete().where(Stations.c.station_id==id))
    #conn.commit()
    return conn.execute(Stations.select()).fetchall()






#index:app