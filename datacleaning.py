#!/usr/bin/env python
# coding: utf-8

# In[44]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np


# In[2]:


df=pd.read_csv("C:\\Users\\Phani\\Downloads\\start_up.csv")


# In[3]:


df


# In[5]:


print(df.info(null_counts=True))


# In[6]:


df.shape


# In[7]:


df.dtypes


# In[12]:


df.apply(lambda x:x)


# In[14]:


df.isnull().sum()


# In[18]:


df.isna().sum()


# In[21]:


pd.to_datetime(df['Date'])


# In[29]:


df[df['Date'].str.contains(r"\d{2}/\d{2}//\d{2}")].replace('22/01//2015','22/01/2015')


# In[32]:


df['Date']=df['Date'].replace('22/01//2015','22/01/2015')


# In[34]:


df['Date']=pd.to_datetime(df['Date'])


# In[35]:


df


# In[40]:


df['AmountInUSD']=df['AmountInUSD'].str.replace(',','')


# In[41]:


df


# In[62]:


df['AmountInUSD']=df['AmountInUSD'].fillna(df['AmountInUSD'].median())


# In[64]:


df['AmountInUSD']=df['AmountInUSD'].astype('int')


# In[69]:


df[df['CityLocation'].isna()]['CityLocation']


# In[71]:


##filling the nan values with not specified
df['CityLocation']=df['CityLocation'].fillna(value='NotSpecific')


# In[72]:


df['IndustryVertical']=df['IndustryVertical'].fillna(value='Other')


# In[75]:


df['CityLocation'].unique()


# In[106]:





# In[102]:


import regex as re
def citY_name(x):
    if re.search(r'/',x):
        return x.split('/')[0].strip()
    else:
        return x.strip()


# In[104]:


df['CityLocation']=df['CityLocation'].apply(citY_name)


# In[107]:


df['CityLocation']=df['CityLocation'].str.lower()


# In[108]:


df


# In[110]:


df.drop(columns=['Remarks','SNo'],inplace=True)


# In[117]:


df['no_of_investors']=df['InvestorsName'].str.split(',').str.len()


# In[123]:


len(df['InvestorsName'].iloc[3].split(','))


# In[126]:


df['InvestorsName'].isna().sum()


# In[128]:


df['InvestorsName']=df['InvestorsName'].fillna(value='empty')


# In[129]:


df['InvestorsName'].isna().sum()


# In[135]:


df['lds']=df['InvestorsName'].apply(lambda x:x.split(','))


# In[140]:


unique_invest=[]
for i in df['lds']:
    for j in i:
        unique_invest.append(j)
d_unq=set(unique_invest)


# In[143]:


unq_inv=list(d_unq)


# In[ ]:


## we have 1 missing value for investment type 


# In[155]:


df['InvestmentType'].fillna(value=st.mode(df['InvestmentType']),inplace=True)


# In[148]:


import statistics as st
st.mode(df['InvestmentType'])


# In[150]:


df['InvestmentType'].isna().sum()


# In[195]:


d=df['StartupName'].str.extract(r"(\w+)\.?[com,in,.]?")


# In[202]:


df['StartupName']=d.iloc[:,0]


# In[208]:


df


# In[210]:


##adding year and month column for yearly analysis


# In[212]:


df['year']=df['Date'].dt.year


# In[213]:


df


# In[215]:


df.to_csv("cleaned_startup.csv")


# In[ ]:




