#!/usr/bin/env python
# coding: utf-8

# ## Samantha Beard
# ### Term Project Milestone 2 - Cleaning/Formatting Flat File Source

# #### Milestone Objective

# Perform at least 5 data transformation and/or cleansing steps to your flat file data. You can do the same transformation multiple times if needed to clean your data. The goal is a clean dataset at the end of the milestone.
# 
# Make sure you clearly label each transformation (Step #1, Step #2, etc.) in your code and describe what it is doing in 1-2 sentences. 

# #### Project / Milestone Explanation

# The goal of my project is to look at if popularity of songs correlates to winning Grammys. 
# 
# source: https://www.kaggle.com/datasets/unanimad/grammy-awards/data

# #### File Set Up

# In[1]:


# import packages

import pandas as pd
import re
import numpy as np


# In[2]:


# import cvs file to dataframe
grammy_awards_df = pd.read_csv('the_grammy_awards.csv')

#show top 5
grammy_awards_df.head()


# In[3]:


# row count
startingRowCount = len(grammy_awards_df.index)
startingRowCount


# In[4]:


num_cols = grammy_awards_df.shape
print(num_cols[1])


# In[5]:


# remove words within parentheses using pandas.series.str.replace to replace each occurrence of () with empty string.
grammy_awards_df['title'] = grammy_awards_df['title'].str.replace(r"\(.*\)","", regex=True)
grammy_awards_df.head()


# In[6]:


grammy_awards_df = grammy_awards_df.drop(columns = ['updated_at'])
grammy_awards_df.head()


# In[7]:


grammy_awards_df.category.unique()


# In[8]:


grammy_awards_df = grammy_awards_df.dropna()


# In[14]:


grammy_awards_df['artist'] = grammy_awards_df['artist'].replace('(','').replace(')','') 


# In[15]:


artists_list = grammy_awards_df.artist.unique()
print((artists_list))


# In[ ]:





# #### Paragraph of the ethical implications of data wrangling specific to your datasource and the steps you completed.

# While some would argue that a version of a song could be more popular than another version, I don't think removing these duplicates is a huge ethical issue as we are going to be comparing this to lists of grammy winning songs and the song title and artist are still the same. Additionally, I don't think there are ethical implications of removing songs with a popularity score of 0.  I think if I had gone with my initial plan of less than than 50 there could be some potential ethical issues. Data wrangling in general can have the ethical implication of adding bias when removing data, however, I believe I have navigated this as best I can while cleaning the data.

# In[ ]:




