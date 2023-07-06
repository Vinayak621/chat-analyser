import re
import pandas as pd
def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_msg':messages,'msg_dates':dates})
    df['msg_dates']=pd.to_datetime(df['msg_dates'], format='%m/%d/%y, %H:%M - ')
    users=[]
    messages=[]
    for message in df['user_msg']:
        entry=re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_msg'],inplace=True)
    df['year']=df['msg_dates'].dt.year
    df['only_date']=df['msg_dates'].dt.date
    df['day_name']=df['msg_dates'].dt.day_name()
    df['month_num']=df['msg_dates'].dt.month
    df['month']=df['msg_dates'].dt.month_name()
    df['day']=df['msg_dates'].dt.day
    df['hour']=df['msg_dates'].dt.hour
    df['minute']=df['msg_dates'].dt.minute
    
    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str('hour')+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    
    df['period']=period
            
    
    return df
    