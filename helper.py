from  urlextract  import URLExtract
from wordcloud import WordCloud
import  pandas as pd 
from collections  import Counter
import re
try:
    extract_rul=URLExtract()
    def fetch_stats(selected_user,df):
        if selected_user=='All':
            #NOTE -  return the total number of meassges
            total_meassges=df.shape[0]
            #NOTE -  Return the total number of words
            total_word=total_words(df)
            #NOTE -  return number of media 
            total_media=df[df['message']=="Media omitted "].shape[0]
            #NOTE - Return the number of link shard
            total_link=link_chat(df)
            return total_meassges,total_word,total_media,total_link
        
        else:

            df=df[df['user']==selected_user]
            #NOTE - return the totl number of measges pertucalr user

            total_meassges=df[df['user']==selected_user].shape[0]
            #NOTE -  Return the total number of words
            total_word=total_words(df)
            #NOTE -  return number of media 
            total_media=df[df['message']=="Media omitted "].shape[0]
            #NOTE - Return the number of link shard 
            total_link=link_chat(df)
            return total_meassges,total_word,total_media,total_link
        #NOTE -  world cloud =============================-----==--
        
    def link_chat(df):
        lin=[]
        for measges in df['message']:
            lin.extend(extract_rul.find_urls(measges))  
        return len(lin)
    
            
    def total_words(df):
        words =[]
        for num_meassges in df['message'] :
                words.extend(num_meassges.split())
        return len(words)
    #NOTE -  return the how chat total persion
    def fetch_busy(df):
        x=df['user'].value_counts().head()
        per=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
        return x,per
    def Creates_wordcloud(selected_user,df):
        if selected_user !='All':
            df=df[df['user']==selected_user]
        wc=WordCloud(width=600,height=600,min_font_size=10,background_color='white')
        df_wc=wc.generate(df['message'].str.cat(sep=" "))
        return df_wc 
    #NOTE - ===============================================================most comman words
    def most_common_words(selected_user,df):
        if selected_user !='All':
            df=df[df['user']==selected_user]
        df =df[df['message']!='Media omitted ']
        wor=[]
        f=open('Hindeenglish.text','r')
        stop_worlds=f.read()
        for mes in df['message']:
            for word in mes.lower().split():

                if word not in stop_worlds:
                    wor.append(word)
        ls=Counter(wor).most_common(20)
        df=pd.DataFrame(ls)
        return  df

    def find_emojis(message):
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F700-\U0001F77F"  # alchemical symbols
                            u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                            u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                            u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                            u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                            u"\U00002702-\U000027B0"  # Dingbats
                            u"\U000024C2-\U0001F251" 
                            "]+", flags=re.UNICODE)
        return emoji_pattern.findall(message)

    def Emoji_helper(selected_user, df):
        if selected_user != 'All':
            df = df[df['user'] == selected_user]

        em = []
        for message in df['message']:
            em.extend(find_emojis(message))

        em_df = pd.DataFrame(Counter(em).most_common(len(Counter(em))))
        return em_df
    # Example usage:
    # selected_user = 'John'  # Replace with the user you are interested in
    # em_df_result = Emoji_helper(selected_user, your_dataframe)
    # print(em_df_result)

    def monthly_time(selected_user,df):
        if selected_user != 'All':
            df = df[df['user'] == selected_user]
    
        timeline=df.groupby(['year','month_num','month']).count().reset_index()
        time=[]
        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
        timeline['time']=time
        return timeline

    def daliy_timeline(selected_user,df):
        if selected_user != 'All':
            df = df[df['user'] == selected_user]
        daly_time=df.groupby('only_date').count()['message'].reset_index()
        return daly_time

    def weakly_timeline(selected_user,df):
        if selected_user != 'All':
            df = df[df['user'] == selected_user]
        
        weak_t=df['day_name'].value_counts()
        return weak_t

    def month_active(selected_user,df):
        if selected_user != 'All':
            df = df[df['user'] == selected_user]
        return df['month'].value_counts()
    def Active_hetmsp(selected_user,df):
        if selected_user != 'All':
            df = df[df['user'] == selected_user]
        active_hetmap=df.pivot_table(index='day_name',columns='peroid',values='message',aggfunc='count').fillna(0)
        return active_hetmap
except Exception as e:
    print(e)














        
        
