
df=pd.read_csv("C:\\Users\\Phani\\Downloads\\start_up.csv")

print(df.info(null_counts=True))
df.shape
df.dtypes
df.isnull().sum()
df.isna().sum()
pd.to_datetime(df['Date'])
df[df['Date'].str.contains(r"\d{2}/\d{2}//\d{2}")].replace('22/01//2015','22/01/2015')
df['Date']=df['Date'].replace('22/01//2015','22/01/2015')
df['Date']=pd.to_datetime(df['Date'])

df['AmountInUSD']=df['AmountInUSD'].str.replace(',','')


df['AmountInUSD']=df['AmountInUSD'].fillna(df['AmountInUSD'].median())


df['AmountInUSD']=df['AmountInUSD'].astype('int')

df[df['CityLocation'].isna()]['CityLocation']

##filling the nan values with not specified
df['CityLocation']=df['CityLocation'].fillna(value='NotSpecific')


df['IndustryVertical']=df['IndustryVertical'].fillna(value='Other')

df['CityLocation'].unique()


import regex as re
def citY_name(x):
    if re.search(r'/',x):
        return x.split('/')[0].strip()
    else:
        return x.strip()

df['CityLocation']=df['CityLocation'].apply(citY_name)

df['CityLocation']=df['CityLocation'].str.lower()


df

df.drop(columns=['Remarks','SNo'],inplace=True)



df['no_of_investors']=df['InvestorsName'].str.split(',').str.len()


len(df['InvestorsName'].iloc[3].split(','))


df['InvestorsName'].isna().sum()



df['InvestorsName']=df['InvestorsName'].fillna(value='empty')



df['InvestorsName'].isna().sum()



df['lds']=df['InvestorsName'].apply(lambda x:x.split(','))



unique_invest=[]
for i in df['lds']:
    for j in i:
        unique_invest.append(j)
d_unq=set(unique_invest)



unq_inv=list(d_unq)



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



df['StartupName']=d.iloc[:,0]



##adding year and month column for yearly analysis



df['year']=df['Date'].dt.year



df.to_csv("cleaned_startup.csv")





