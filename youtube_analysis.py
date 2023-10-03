#!/usr/bin/env python
# coding: utf-8

# # Youtube channel analysis

# In[138]:


pip install --upgrade google-api-python-client


# In[139]:


import pandas as pd
from googleapiclient.discovery import build
import seaborn as sns


# In[140]:


api_key="AIzaSyDffLbtCHpmlG5QnJkW4chzzBEGPtxWpM0"
channel_ids=["UCnz-ZXXER4jOvuED5trXfEA",#TechTFQ
           "UCpQ34afVgk8cRQBjSJ1xuJQ",#madfit
           "UCneyi-aYq4VIBYIAQgWmk_w",#RanveerAllahbadia
           "UCPxMZIFE856tbTfdkdjzTSQ",#beerbiceps
           "UCQTmoQ_S26PlmDoXujZpbYQ"#timkim
           ]

youtube = build("youtube","v3",developerKey=api_key)


# # function to get channel statistics

# In[144]:


# exract the channel details
def get_channel_stats(youtube,channel_ids):
    all_data=[]
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids))
    response = request.execute()
    
    for i in range(len(response["items"])):
        data = dict(channel_name=response["items"][i]['snippet']["title"],
                  subsribers=response["items"][i]['statistics']["subscriberCount"],
                  views= response["items"][i]['statistics']["viewCount"],
                  total_videos= response["items"][i]['statistics']["videoCount"],
                  playlist_id=response["items"][i]['contentDetails']["relatedPlaylists"]["uploads"])
        all_data.append(data)
    return all_data


# In[145]:


channel_statistics=get_channel_stats(youtube,channel_ids)


# In[146]:


channel_data=pd.DataFrame(channel_statistics)


# In[147]:


channel_data


# In[148]:


channel_data["subsribers"]=pd.to_numeric(channel_data["subsribers"])
channel_data["views"]=pd.to_numeric(channel_data["views"])
channel_data["total_videos"]=pd.to_numeric(channel_data["total_videos"])


# In[149]:


channel_data


# In[150]:


channel_data.dtypes


# In[151]:


sns.set(rc={"figure.figsize":(7,4)})
ax=sns.barplot(x="channel_name",y="subsribers",data=channel_data)


# In[152]:


sns.set(rc={"figure.figsize":(7,4)})
ax=sns.barplot(x="channel_name",y="views",data=channel_data)


# In[153]:


sns.set(rc={"figure.figsize":(7,4)})
ax=sns.barplot(x="channel_name",y="total_videos",data=channel_data)


# In[167]:


playlist_id=channel_data.loc[channel_data['channel_name']=="BeerBiceps","playlist_id"].iloc[0]


# In[168]:


playlist_id


# In[169]:


##function to get video id
def get_video_ids(youtube,playlist_id):
    
    request=youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50)
    response=request.execute()
    
    video_ids=[]
    for i in range(len(response["items"])):
        video_ids.append(response["items"][i]["contentDetails"]["videoId"])
        
    next_page_token=response.get("nextPageToken")
    more_pages=True
    
    while more_pages:
        if next_page_token is None:
            more_pages=False
        else:
            request=youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)
            response=request.execute()
            
            for i in range(len(response["items"])):
                video_ids.append(response["items"][i]["contentDetails"]["videoId"])
                
            next_page_token=response.get("nextPageToken")
    return (video_ids)
    


# In[170]:


video_ids = get_video_ids(youtube,playlist_id)


# In[171]:


video_ids


# # functions to get video details

# In[172]:


def get_video_details(youtube,video_ids):
    all_video_stats=[]
    
    for i in range(0,len(video_ids),50):
        request = youtube.videos().list(
                part="snippet,statistics",
                id=','.join(video_ids[i:i+50]))
        response = request.execute()
        
        for video in response['items']:
            video_stats=dict(Title=video['snippet']['title'],
                                    Published_date=video["snippet"]['publishedAt'],
                                    Views=video['statistics']['viewCount'],
                                    likes=video['statistics']['likeCount'],
                                    comments=video['statistics']['commentCount'])
            
            all_video_stats.append(video_stats)
            
    return (all_video_stats)


# In[173]:


video_details=get_video_details(youtube,video_ids)


# In[174]:


video_data=pd.DataFrame(video_details)


# In[175]:


video_data


# In[176]:


video_data["Published_date"]=pd.to_datetime(video_data["Published_date"]).dt.date
video_data["Views"]=pd.to_numeric(video_data["Views"])
video_data["likes"]=pd.to_numeric(video_data["likes"])
video_data["comments"]=pd.to_numeric(video_data["comments"])
video_data


# In[177]:


top10_videos=video_data.sort_values(by=["Views"],ascending=False).head(10)


# In[178]:


top10_videos


# In[179]:


ax1=sns.barplot(x="Views",y="Title",data=top10_videos)


# In[180]:


video_data


# In[181]:


video_data["Month"]=pd.to_datetime(video_data["Published_date"]).dt.strftime('%b')


# In[182]:


video_data


# In[183]:


videos_per_month=video_data.groupby('Month',as_index=False).size()


# In[184]:


videos_per_month


# In[185]:


sort_order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


# In[186]:


videos_per_month.index=pd.CategoricalIndex(videos_per_month["Month"],categories=sort_order,ordered=True)


# In[187]:


videos_per_month=videos_per_month.sort_index()


# In[188]:


ax2=sns.barplot(x="Month",y="size",data=videos_per_month)


# In[ ]:




