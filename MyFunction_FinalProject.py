#!/usr/bin/env python
# coding: utf-8

# ## IMPORTING LIBRARIES

# In[77]:


import matplotlib
import matplotlib.dates as mdates
import warnings
import pandas as pd
from pandas.io import sql
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import timeit
from sqlalchemy import *
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

warnings.filterwarnings('ignore')


# ## INITIAL CLEANING FUNCTION

# In[78]:


def initial_cleaning(df):
    unused_rows_list=[0,1,2,3,4]
    column_header_row=4
    df.rename(columns=df.iloc[column_header_row],inplace=True)
    df.drop(df.index[[unused_rows_list]],inplace=True)
    df=df.reset_index(drop=True)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    return df


# # DATABASE FUNCTIONS

# In[79]:


def save_to_sqlite(df,tablename):
    cnx=sqlite3.connect('internship.db')
    sqlite_table=tablename
    df.to_sql(sqlite_table,cnx, if_exists='fail')
    p2 = pd.read_sql('select * from '+tablename, cnx)
    print(p2.head(5))


# In[80]:


def save_to_Mysql(df,tablename):
    username="root"
    password="root"
    host="localhost"
    database="internship_db_mysql"
    
    engine = create_engine("mysql+pymysql://" + username + ":" + password + "@" + host + "/"+ database)
    df.to_sql(tablename, con = engine, if_exists = 'fail',index = False, chunksize = 1000)  


# In[81]:



def save_to_Mariadb(df,tablename):
    engine = create_engine("mariadb+mariadbconnector://root:root@127.0.0.1:3307/internship_db_maria")
    df.to_sql(tablename, con = engine, if_exists = 'fail',index = False, chunksize = 1000)


# In[82]:


def MSQL_con():
    username="root"
    password="root"
    host="localhost"
    database="internship_db_mysql"
    con_mysql = create_engine("mysql+pymysql://" + username + ":" + password + "@" + host + "/"+ database)
    connection=con_mysql.connect().connection
    cursor=connection.cursor()
    return cursor,con_mysql
    


# In[83]:


def Sqlite_db():
    cnx=sqlite3.connect('internship.db')
    cursor=cnx.cursor()
    return cursor


# In[84]:


def Mariadb_con():
    con_maria = create_engine("mariadb+mariadbconnector://root:root@127.0.0.1:3307/internship_db_maria")
    connection=con_maria.connect().connection
    cursor=connection.cursor()
    return cursor


# In[85]:


def TimeOfExecutionRecording(SETUP_CODE,TEST_CODE1,TEST_CODE2,TEST_CODE3,TEST_CODE4,TEST_CODE5,TEST_CODE6):
    TEST_CODE=pd.DataFrame(timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE1,
                    repeat=100,
                          number = 1),columns =['Query1'])
    TEST_CODE['Query2']=pd.DataFrame(timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE2,
                    repeat=100,
                          number = 1))
    TEST_CODE['Query3']=pd.DataFrame(timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE3,
                    repeat=100,
                          number = 1))
    TEST_CODE['Query4']=pd.DataFrame(timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE4,
                    repeat=100,
                          number = 1))
    TEST_CODE['Query5']=pd.DataFrame(timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE5,
                    repeat=100,
                          number = 1))
    TEST_CODE['Query6']=pd.DataFrame(timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE6,
                    repeat=100,
                          number = 1))
    return TEST_CODE


# ## FUNCTIONS FOR LINEAR REGRESSION 

# In[86]:


def Dataset_preparation_for_LR_state1(dayonedaily2_df):
     # droping unwanted coloumn
    dayonedaily2_df["D1_Actual_Time"]=pd.to_datetime(dayonedaily2_df["D1_Actual_Time"],format='%H:%M:%S').dt.time
    dayonedaily2_df["D1_Working_Time"]=pd.to_datetime(dayonedaily2_df["D1_Working_Time"],format='%H:%M:%S').dt.time
    dayonedaily2_df.insert(0,'ID',range(1,1+len(dayonedaily2_df)))
    dayonedaily2_df=dayonedaily2_df[['ID','D1_Hcode','D1_Origin','D1_Dest','D1_Location','D1_Planned_Activity','D1_Working_Var']]
    dayonedaily2_df=dayonedaily2_df.dropna()
    # Getting the first row of each head code
    df=dayonedaily2_df.groupby(['D1_Hcode']).first().reset_index()
    H=['O']
    A=list(df.loc[~df['D1_Planned_Activity'].isin(H),'D1_Hcode'])
    dayonedaily2_df=dayonedaily2_df[~dayonedaily2_df['D1_Hcode'].isin(A)]# Filtering out headcode which is not having Origin in the first value of  D1_planned_Activity for proper data distibution
    
    df=dayonedaily2_df.groupby(['D1_Hcode']).nth(1).reset_index()# Getting the 2nd row of each head code
    H=['A','P']
    A=list(df.loc[~df['D1_Planned_Activity'].isin(H),'D1_Hcode'])
    dayonedaily2_df=dayonedaily2_df[~dayonedaily2_df['D1_Hcode'].isin(A)] #Filtering out values which is not A and P in second row
    
    df=dayonedaily2_df.groupby(['D1_Hcode']).last().reset_index() # Getting the last row of each head code
    H=['T']
    A=list(df.loc[~df['D1_Planned_Activity'].isin(H),'D1_Hcode'])
    dayonedaily2_df=dayonedaily2_df[~dayonedaily2_df['D1_Hcode'].isin(A)]
    
    L=['D']
    df1=dayonedaily2_df[~dayonedaily2_df['D1_Planned_Activity'].isin(L)] #Filtering out values which is d from entire dataset
    
    
    return df1


# In[87]:


def Dataset_preparation_for_LR_stage2(dayonedaily2_df):
    
    #conversion into Dataset with D1_Working_Var1,D1_Working_Var2,D1_Working_Var3,D1_Working_Var_Final
    
    df_trail=dayonedaily2_df[['ID','D1_Hcode','D1_Origin','D1_Dest','D1_Location','D1_Planned_Activity','D1_Working_Var']].groupby(['D1_Hcode']).first().reset_index().sort_values(by=['ID'],ascending=True)
    df2=dayonedaily2_df[['ID','D1_Hcode','D1_Working_Var']].groupby(['D1_Hcode']).nth(1).reset_index().sort_values(by=['ID'])
    df_trail=pd.merge(df_trail,df2,on="D1_Hcode",how="left",suffixes=['_1','_2'])
    df3=dayonedaily2_df[['ID','D1_Hcode','D1_Working_Var']].groupby(['D1_Hcode']).nth(2).reset_index().sort_values(by=['ID'])
    df_trail=pd.merge(df_trail,df3,on="D1_Hcode",suffixes=['_T3'],how="left")
    df_T=dayonedaily2_df[['ID','D1_Hcode','D1_Working_Var']].groupby(['D1_Hcode']).last().reset_index().sort_values(by=['ID'])
    df_trail=pd.merge(df_trail,df_T,on="D1_Hcode",suffixes=['_1L','_2L'],how="left")

    df_trail=df_trail.drop(["ID_1","ID_2","ID_1L","ID_2L","D1_Planned_Activity","D1_Origin","D1_Dest","D1_Location"],axis=1)


    df_trail.rename(columns={'D1_Working_Var_1L':'D1_Working_Var_3','D1_Working_Var_2L':'D1_Working_Var_Final'},inplace=True)
    return df_trail


# In[88]:


def Dataset_preparation_for_LR_stage3_Mapping(dayonedaily2_df):
    #Masking values to 0 and 1 
    X=dayonedaily2_df[['D1_Working_Var_1','D1_Working_Var_2','D1_Working_Var_3']]
    Y=dayonedaily2_df[['D1_Working_Var_Final']]
    X=X.mask(X<=0,0)
    X=X.mask(X>0,1)
    Y=Y.mask(Y<=0,0)
    Y=Y.mask(Y>0,1)
    
    
    v=(Y['D1_Working_Var_Final']==X['D1_Working_Var_1'])

    v=Y.D1_Working_Var_Final[Y.D1_Working_Var_Final == X.D1_Working_Var_1].index.tolist()
    
    X= X.loc[v]
    
    Y=Y.loc[v]
    return X,Y


# In[ ]:





# In[ ]:





# In[ ]:




