from urlextract import URLExtract
extract=URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]
    words=[]
    for msg in df['message']:
        words.extend(msg.split())
        
    media_msg=df[df['message']== '<Media omitted>\n'].shape[0]
    
    links=[]
    for msg in df['message']:
        links.extend(extract.find_urls(msg))
    
    return num_messages,len(words),media_msg,len(links)
    
    
def fetch_active_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','user':'percent'})
    return x,df
    


def create_wrd_cld(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    
    words=[]
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    return_df=pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_used(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    
    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
        
    timeline=df.groupby(['year', 'month_num','month']).count()['message'].reset_index()
    
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+" "+str(timeline['year'][i]))
        
    timeline['time']=time
        
    return timeline    

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
        
def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
        
    return df['month'].value_counts()

def heatmap_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    hac=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    
    return hac
    
    
    