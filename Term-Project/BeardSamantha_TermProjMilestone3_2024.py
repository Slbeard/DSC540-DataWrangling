#!/usr/bin/env python
# coding: utf-8

# ## Samantha Beard
# 
# #### Term Project Milestone 3: Cleaning/Formatting Website Data

# ### Setup

# In[2]:


# import libraries
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import codecs
import os


# In[3]:


# import website
url = 'https://en.wikipedia.org/wiki/Grammy_Awards'
page = requests.get(url)
grammy_soup = BeautifulSoup(page.text, 'html', features='lxml')


# In[4]:


# find table that I am wanting to use
grammy_edition_table = grammy_soup.find_all('table', class_ = 'wikitable')[0]


# In[5]:


# functions to parse the wikitable

# this function will determine how many rows and columns should be in the table to prevent data from being empty
def pre_process_table(grammy_edition_table):
    # <tr> = table row
    rows = [x for x in grammy_edition_table.find_all('tr')]

    num_rows = len(rows)

    # get an initial column count. Most often, this will be accurate
    # <th> = table header and <td> = table data
    num_cols = max([len(x.find_all(['th','td'])) for x in rows])

    # I did not see column spans, however, to ensure that all the data is returned we will check
    header_rows_set = [x.find_all(['th', 'td']) for x in rows if len(x.find_all(['th', 'td']))>num_cols/2]

    num_cols_set = []

    for header_rows in header_rows_set:
        num_cols = 0
        for cell in header_rows:
            row_span, col_span = get_spans(cell)
            num_cols+=len([cell.getText()]*col_span)

        num_cols_set.append(num_cols)

    num_cols = max(num_cols_set)

    return (rows, num_rows, num_cols)                          
    

# function to get which rows and columns have spans
def get_spans(cell):
        if cell.has_attr('rowspan'):
            rep_row = int(cell.attrs['rowspan'])
        else: # ~cell.has_attr('rowspan'):
            rep_row = 1
        if cell.has_attr('colspan'):
            rep_col = int(cell.attrs['colspan'])
        else: # ~cell.has_attr('colspan'):
            rep_col = 1 

        return (rep_row, rep_col)

# function to apply the data to all rows in span
def process_rows(rows, num_rows, num_cols):
    data = pd.DataFrame(np.ones((num_rows, num_cols))*np.nan)
    for i, row in enumerate(rows):
        try:
            col_stat = data.iloc[i,:][data.iloc[i,:].isnull()].index[0]
        except IndexError:
            print(i, row)

        for j, cell in enumerate(row.find_all(['td', 'th'])):
            rep_row, rep_col = get_spans(cell)

            #print("cols {0} to {1} with rep_col={2}".format(col_stat, col_stat+rep_col, rep_col))
            #print("\trows {0} to {1} with rep_row={2}".format(i, i+rep_row, rep_row))

            #find first non-na col and fill that one
            while any(data.iloc[i,col_stat:col_stat+rep_col].notnull()):
                col_stat+=1
            
            data.iloc[i:i+rep_row,col_stat:col_stat+rep_col] = cell.getText(strip = True) # strip will remove /n 
            if col_stat<data.shape[1]-1:
                col_stat+=rep_col
    return data


# In[6]:


# call functions
rows, num_rows, num_cols = pre_process_table(grammy_edition_table)
# convert into df
grammy_edition_df = process_rows(rows, num_rows, num_cols)


# In[7]:


grammy_edition_df.head(10)


# ### Step 1
# The first step will be to update the headers from the column numbers to the column headers

# In[8]:


# what are the current column names
list(grammy_edition_df.columns)


# In[9]:


# replace column names with first row from df
grammy_edition_df.columns = grammy_edition_df.iloc[0]


# In[10]:


# remove first row so that there isn't a duplicate
grammy_edition_df = grammy_edition_df[1:]


# In[11]:


list(grammy_edition_df.columns)


# In[12]:


# The header Viewers(in millions) should have a space between the s and (
grammy_edition_df.rename(columns={'Viewers(in millions)':'Viewers (in millions)'}, inplace=True)


# In[13]:


list(grammy_edition_df.columns)


# ### Step 2
# The next step will be to add spacing on either side of ampersand using string replacement

# In[14]:


grammy_edition_df.head(15)


# In[15]:


grammy_edition_df['Venue City'] = grammy_edition_df['Venue City'].str.replace(r"&"," & ", regex=True)


# In[16]:


grammy_edition_df.head(10)


# ### Step 3
# Next will be adding spaces after commas using string replacement

# In[17]:


grammy_edition_df['Venue City'] = grammy_edition_df['Venue City'].str.replace(r",",", ", regex=True)


# In[18]:


grammy_edition_df.head(10)


# ### Step 4
# Again updating the string of Venue city as NashvilleandNew York is difficult to read.  Additionally, there is are inconsistencies in '&' vs 'and' so making that consistent with an ampersand - using string replacement

# In[19]:


grammy_edition_df['Venue City'] = grammy_edition_df['Venue City'].str.replace(r"eandN","e & N", regex=True)


# In[23]:


grammy_edition_df.head(10)


# ### Step 5
# I also need to add a space to the Venue column for the first few that don't have a space between including and Beverly using string replacement

# In[ ]:


grammy_edition_df.columns = grammy_edition_df.columns.str.replace('Viewers(in millions)', 'Viewers (in millions)', regex=True)


# In[24]:


grammy_edition_df['Venue'] = grammy_edition_df['Venue'].str.replace(r"gB","g B", regex=True)


# In[26]:


grammy_edition_df


# ### Step 6
# Removing numbers in brackets that were links to other pages using string replacement

# In[31]:


grammy_edition_df['Viewers (in millions)'] = grammy_edition_df['Viewers (in millions)'].str.replace(r"\[.*\]","", regex=True)
grammy_edition_df['Venue'] = grammy_edition_df['Venue'].str.replace(r"\[.*\]","", regex=True)


# In[32]:


grammy_edition_df


# In[ ]:




