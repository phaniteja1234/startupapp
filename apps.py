import streamlit as st
import  pandas as pd
import  numpy as np
import  plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(
    page_title="Start up analysis",
    page_icon="🧊",
    layout="wide",
)
st.sidebar.title('startup funding')
opt=st.sidebar.selectbox('select any of the one',['over analysis','startup','Investor','Timeseries_analysis'])
df=pd.read_csv('cleaned_startup.csv')
df['lds']=df['InvestorsName'].apply(lambda x:x.split(','))
def overall():
    c1,c2,c3=st.columns(3)
    with c1:
        tot=round(df['AmountInUSD'].sum())
        st.metric('Total investments money in usd',tot)
    with c2:
        name=df.groupby("StartupName")['AmountInUSD'].sum().sort_values(ascending=False).head(1).index[0]
        amt=df.groupby("StartupName")['AmountInUSD'].sum().sort_values(ascending=False).head(1).values[0]
        st.metric(f"maximum investment on {name}",amt)
    with c3:
        avg=round(df.groupby("StartupName")['AmountInUSD'].sum().mean())
        st.metric("average investment",avg)
    yd = df.groupby("year")['AmountInUSD'].sum().reset_index()
    yd['amount'] = round(yd['AmountInUSD'])
    st.markdown(f'<h1 style="color:#ADD8E6;font-size:24px;">{"year wise investment"}</h1>',
                unsafe_allow_html=True)
    fig = px.line(yd, x='year', y='amount')
    st.plotly_chart(fig, theme=None, use_container_width=True)
    col1,col2=st.columns(2)
    with col1:
        ##Top 10 startups with most fundings
        st.markdown(
            f'<h1 style="color:#ADD8E6;font-size:24px;">{"Top 10 startups with most fundings"}</h1>',
            unsafe_allow_html=True)
        st.dataframe(df.groupby('StartupName')['AmountInUSD'].sum().sort_values(ascending=False).head(10))
    with col2:
        ## kind of investment did the top10 startups got
        st.markdown(
            f'<h1 style="color:#ADD8E6;font-size:24px;">{"kind of investment did the top10 startups got"}</h1>',
            unsafe_allow_html=True)
        top_10 = list(df.groupby('StartupName')['AmountInUSD'].sum().sort_values(ascending=False).head(10).index)
        top_ten = df[df['StartupName'].isin(top_10)]
        st.dataframe(pd.crosstab(top_ten['StartupName'], top_ten['InvestmentType']))
    col1, col2 = st.columns(2)
    with col1:
        ####companies with most no of investments
        st.markdown(
            f'<h1 style="color:#ADD8E6;font-size:24px;">{"companies with more no of investors"}</h1>',
            unsafe_allow_html=True)
        new_sd = df.drop_duplicates(subset=['StartupName', 'InvestorsName'], keep='first').groupby('StartupName')[
            'no_of_investors'].sum().sort_values(ascending=False)
        new_sd = new_sd.reset_index().head(10)
        fig5 = px.bar(new_sd, x='StartupName', y='no_of_investors')
        st.plotly_chart(fig5, theme=None, use_container_width=True)
    with col2:
        ###Density estimation for no of investor
        st.markdown(
            f'<h1 style="color:#ADD8E6;font-size:24px;">{"Density estimation for no of investors"}</h1>',
            unsafe_allow_html=True)
        new_sd = df.drop_duplicates(subset=['StartupName', 'InvestorsName'], keep='first').groupby('StartupName')[
            'no_of_investors'].sum().sort_values(ascending=False)
        new_df = new_sd.reset_index()
        fig = plt.figure(figsize=(4, 4))
        sns.kdeplot(data=new_df, x='no_of_investors')
        st.pyplot(fig)
    ##top 10 mostly funded industry sector
    st.markdown(
            f'<h1 style="color:#ADD8E6;font-size:24px;">{"top 10 mostly funded industry sector"}</h1>',
            unsafe_allow_html=True)
    ind = df.groupby("IndustryVertical")['AmountInUSD'].sum().sort_values(ascending=False).head(10).reset_index()
    st.dataframe(ind)
    col1, col2 = st.columns(2)
    with col1:
        ##Top 10 Investors with highest funding amount¶
        st.markdown(
            f'<h1 style="color:#ADD8E6;font-size:24px;">{"##Top 10 Investors with highest funding amount¶"}</h1>',
            unsafe_allow_html=True)
        df['lds'] = df['InvestorsName'].apply(lambda x: x.split(','))
        unique_invest = []
        for i in df['lds']:
            for j in i:
                unique_invest.append(j)
        d_unq = set(unique_invest)
        d = {}
        for i in list(d_unq):
            amount = df[df['InvestorsName'].str.contains(i)]['AmountInUSD'].sum()
            d[i] = amount
        invest = pd.Series(d)
        invest = invest.iloc[1:]
        st.dataframe(invest.sort_values(ascending=False).head(10))
        tg = list(invest.sort_values(ascending=False).head(10).index)
    with col2:
        t = pd.DataFrame()
        for i in tg:
            new_df = df[df['InvestorsName'].str.contains(i)]
            new_df['unique'] = i
            t = t.append(new_df)
        t.groupby("IndustryVertical")['unique'].count().sort_values(ascending=False).head(10)
        sd = t.groupby("IndustryVertical")['unique'].count().sort_values(ascending=False).head(10)
        sd = sd.reset_index()
        fig2 = px.pie(sd, values="unique", names="IndustryVertical")
        st.markdown(
            f'<h1 style="color:#ADD8E6;font-size:24px;">{"##sectors opted by top investors"}</h1>',
            unsafe_allow_html=True)
        st.plotly_chart(fig2,width=10000,height=10000, use_container_width=True)
    # in which sector there are most startups
    st.markdown(
        f'<h1 style="color:#ADD8E6;font-size:24px;">{"##sectors with most startups "}</h1>',
        unsafe_allow_html=True)
    d = df['IndustryVertical'].value_counts().head(5)
    f = df.groupby('InvestmentType').sum()['AmountInUSD']
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    labels = [d.index, f.index]
    size = [d.values, f.values]
    colors = [['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'pink'], ['green', 'pink', 'red', 'yellow']]
    plt.axis('equal')
    explode = ((0.1, 0, 0, 0, 0), (-0.3, 0.3, 0.1, 0.1,0.1))
    ax[0].pie(size[0], explode=explode[0], labels=labels[0], colors=colors[0],
              autopct='%1.1f%%', shadow=True, startangle=140)
    ax[1].pie(size[1], labels=labels[1], colors=colors[1], autopct='%1.5f%%', shadow=True,
              startangle=140)
    st.pyplot(fig)
    ss = df.groupby("CityLocation")['StartupName'].count().reset_index()
    ss.rename(columns={"StartupName": "count"}, inplace=True)
    fig=px.treemap(ss, path=['CityLocation'], values='count')
    st.markdown(
        f'<h1 style="color:#ADD8E6;font-size:24px;">{"##startup distribution across various cities "}</h1>',
        unsafe_allow_html=True)
    st.plotly_chart(fig, theme=None, use_container_width=True)
    st.subheader("CONCLUSION")
    st.text(''' 
    1. There were more than 2000 new startups funded in the year between 2015-2017
    2.Paytm and Flipkart were funded most
    3.Top 10 investments are made through private equity
    4.There were more than 1900 unique investors
    5.Ola was Funded most frequent number of times.
    6.Average funding was most in 2017
    7.Top investors funded ecommerce and consumer internet most in terms of amount.
    8.Consumer internet was the top most choice for all investors.
    9.Banglore had the most average funding
    10.Maximum Total funding was generated in the year 2015 and then it slowly decreased with increase in years
    ''')
def load_invest(inv):
    st.title(inv)
    st.subheader(f"recent investment details of {inv}")
    try:
        st.dataframe(df[df['InvestorsName'].str.contains(inv)].sort_values(by='Date', ascending=False).head(5)[
            ['Date', 'StartupName', 'IndustryVertical', 'CityLocation', 'AmountInUSD']])
    except:
        st.markdown("Insufficient data please try another ")
    col1,col2=st.columns(2)
    with col1:
        st.subheader(f"top  investment made by {inv}")
        d = df[df['InvestorsName'].str.contains(inv)].groupby('StartupName')['AmountInUSD'].sum().sort_values(ascending=False).reset_index().head(10)
        fig = px.bar(d, x='StartupName', y='AmountInUSD')
        fig.update_xaxes(title_font=dict(size=20))
        fig.update_yaxes(title_font=dict(size=20))
        fig.update_layout(
            font=dict(
                family="Courier New, monospace",
                size=7,  # Set the font size here
                color="white"
            )
        )
        st.plotly_chart(fig, theme=None, use_container_width=True)
    st.subheader(f"investments made by {inv} at different sectors")
    t = df[df['InvestorsName'].str.contains(inv)].groupby('IndustryVertical')['AmountInUSD'].sum().reset_index().head(10)
    t = t.rename(columns={"IndustryVertical": "sector"})
    fig = px.pie(t, values='AmountInUSD', names='sector')
    st.plotly_chart(fig, width=2000, height=2000, use_container_width=True)
    coln1, coln2 = st.columns(2)
    with coln1:
        st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{"year on year investment made by " + "" + inv}</h1>',
                    unsafe_allow_html=True)
        y = df[df['InvestorsName'].str.contains(inv)].groupby('year')['AmountInUSD'].sum().reset_index()
        fig3 = px.line(y, x='year', y='AmountInUSD')
        st.plotly_chart(fig3, theme=None, use_container_width=True)
def satrtup_analysis(star):
    st.title(star)
    col1, col2 = st.columns(2)
    with col1:
        try:
           cit = df[df['StartupName'].str.contains(star)]['CityLocation'].value_counts().sort_values(ascending=False).head(
            1).index[0]
           st.metric("Founded in", cit)
        except:
            cit=df[df['StartupName'].str.contains(star)]['CityLocation'].head(1).values[0]
            st.metric("Founded in", cit)

    with col2:
        try:
           typ = df[df['StartupName'].str.contains(star)]['SubVertical'].value_counts().sort_values(ascending=False).head(
            1).index[0]
           st.metric("industry vertical", typ)
        except:
            typ = df[df['StartupName'].str.contains(star)]['SubVertical'].head(1).values[0]
            st.metric("industry vertical", typ)
    col1,col2=st.columns(2)
    with col1:
       tot=round(df[df['StartupName'].str.contains(star)]['no_of_investors'].mean())
       st.metric("no of investors",tot)

    st.subheader(f"max investment made on {star}")
    d = df[df['StartupName'].str.contains(star)]
    st.dataframe(d.groupby('InvestorsName')['AmountInUSD'].sum().sort_values(ascending=False).head(1).reset_index())
    st.subheader(f"avg investment  on {star}")
    d = df[df['StartupName'].str.contains(star)]
    st.write(d.groupby('InvestorsName')['AmountInUSD'].sum().mean())
    st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{f"types of funds recived by{star}"}</h1>',
                unsafe_allow_html=True)
    d = df[df['StartupName'].str.contains(star)]
    n = d.groupby("InvestmentType")['InvestmentType'].count()
    dd = pd.DataFrame(n)
    dd.rename_axis("type of investment", inplace=True)
    dd= dd.reset_index()
    fig=px.pie(dd, values='InvestmentType', names='type of investment')
    st.plotly_chart(fig, theme=None, use_container_width=True)
    n = df[df['StartupName'].str.contains(star)].groupby("year")['AmountInUSD'].sum().reset_index()


def time_series(x):
    col1,col2=st.columns(2)
    with col1:
       unq=len(df[df.year == x]['StartupName'].unique())
       st.metric(f"total number of unique startups funded in {x} is ",unq)
    with col2:
       amount=df[df['year'] == 2017]['AmountInUSD'].sum()
       st.metric(f"Total funding in {x}",amount)
    st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{"quarterly investments"}</h1>',
                unsafe_allow_html=True)
    new_df=df.set_index('Date')
    year = new_df.loc[str(x)]
    year = year.resample('q').sum()
    year['quarter'] = year.index.quarter
    fig = px.bar(year, x='quarter', y='AmountInUSD', color='quarter')
    st.plotly_chart(fig, theme=None, use_container_width=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['month'] = df['Date'].dt.month
    y_df=df[df['year']==x]
    st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{f"Funding Variation Per Month in the year  {x}"}</h1>',
                unsafe_allow_html=True)
    fig = plt.figure(figsize=(20, 7))
    ts_month = y_df.groupby(['year', 'month']).agg({'AmountInUSD': 'sum'})['AmountInUSD']
    ts_month.plot(linewidth=4, color='crimson', marker="o", markersize=10, markerfacecolor='olive')
    plt.ylabel('USD in Billions')
    plt.xlabel('Month')
    plt.title(f'Funding Variation Per Month in the year{x}')
    st.pyplot(fig)
    st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{f"types of funding in the year {x}"}</h1>',
                unsafe_allow_html=True)
    fund_df = df[df.year == x]['InvestmentType'].value_counts().reset_index().rename(
        columns={"index": "type of fundings"})
    fig=px.pie(fund_df,values='InvestmentType',names='type of fundings')
    st.plotly_chart(fig)
    if x==2015:
        st.subheader("Investment type in 2015")
        st.text('''
        Private equity is more dispersed according to amount funded
and more amount is invested through private equity per startup on the otherhand seed funding is less dispersed according to amount funded and low amount is funded using this but frequency of seed funding is more as compared to private equity
No dept funding occured in 2015
        ''')
    elif x == 2016:
        st.subheader("Investment type in 2016")
        st.text('''
    Private equity is more dispersed according to amount funded and more amount is invested through private equity per startup on the otherhand seed funding is less dispersed according to amount funded and low amount is funded using this but frequency of seed funding is more as compared to private equity
    As compared to 2015v seed funding has slightly more deviated
     No dept funding and crowd funding occured in 2016
    ''')
    elif x==2017:
        st.subheader("Investment type in 2017")
        st.text('''
        Private Equity is not so dispersed as compared to previous two years
Debt funding slightly taken place
        ''')

    if x==2015:
       st.subheader(f"Insights of {x}")
       st.text('''
    Insights of 2015
   Below we can visualize that total funding reached to its peak between the months of june - july and Aug - Sep
   End week of july was most attracted to investments
   Quarter 3 was seen as the most funded quarter of 2015
    ''')
    elif x==2016:
        st.subheader(f"Insights of {x}")
        st.text('''
   It seems to be january and augest was the most funding month in 2016
   A sudden increase is witnessed in the month of july - August

   june seems to be the decline in funding may be due to goverment administration

   further after september uniform low funding due to demonetization of indian currency

   early weeeks of augest seems to be the most funding time

   An inverse relation among funding by Quarter
        ''')
    elif x==2017:
        st.subheader(f"Insights of {x}")
        st.text('''
        It seems to be feb and march was the most funding amount in 2017
        A sudden decrease is witnessed in the month of july - August
        quarter 1 was seen as the most funded quarter of 2017
        ''')



if opt=='over analysis':
    st.title('over analysis')
    overall()
elif opt=="Investor":
    st.title('Investor analysis')
    unique_invest = []
    for i in df['lds']:
        for j in i:
            unique_invest.append(''.join(j))
    d_unq = list(set(unique_invest))
    op3 = st.sidebar.selectbox('select any one of the investor',d_unq)
    bt2 = st.sidebar.button("find the investor details")
    if bt2:
        load_invest(op3)
elif opt=='startup':
    op2 = st.sidebar.selectbox('select any of the one', df['StartupName'].unique().tolist())
    st.title('Startup Analysis..')
    bt1 = st.sidebar.button("find the startup details")
    if bt1:
        satrtup_analysis(op2)
else:
    op3=st.sidebar.selectbox('select any of the given year',df.year.unique().tolist())
    st.title("Time series analysis")
    df['Date'] = pd.to_datetime(df['Date'])
    bt2=st.sidebar.button(f"find the time series analysis of {op3}")
    if bt2:
        time_series(op3)
