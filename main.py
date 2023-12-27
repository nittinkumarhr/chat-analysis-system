import re
import pandas as pd
try:
    def precess_data(data):
            data = data.replace('\n', '')
            data = data.replace('\r', '')
            data = data.replace('\\n', '')
            data = data.replace(r"'", '')
            data = data.replace(r"''", '')
            data = data.replace(r"]", '')
            data = data.replace(r",", '')
            data = data.replace(r"<", '')
            data = data.replace(r">", '')
            return data
    def get_data(data):
        
        f =data.split('\n')
        data=f[1:]
    
        data=str(data)
        #!SECTION => find the date and time 
        p='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

        match_Date_time = re.findall(p,data)

        # print(match_Date_time)

        #!SECTION => Find the message 

        match_Message = re.split(p,data)[1:]
        
        # m=match_Message.pop(1



        user=[]
        mes=[]
        for meassage in match_Message:
            entry= re.split('([\w\W]+?):\s',meassage)#LINK - uses regular expressions to extract entries starting with a colon and ending with a whitespace character from a message
            
            if entry[1:]:#user name 
                entry = [precess_data(e) for e in entry]
                
                user.append(entry[1:][0])
                mes.append(entry[2])
            else:
                user.append('group_noitfication') 
                mes.append(entry[0])
        if len(mes)==len(user)==len(match_Date_time):
        
            df = pd.DataFrame({
                    'meassage_date': match_Date_time,
                    'user': user,
                    'message': mes
                })
            df['meassage_date']=pd.to_datetime(df['meassage_date'],format="%m/%d/%y, %H:%M - ")
            df.rename(columns={'meassage_date':'date'},inplace=True)
            
        else:
            print("ERROR MESSAGE :++++++++++++++++++++++")
            
        
        df['year']=df['date'].dt.year
        df['month']=df['date'].dt.month_name()
        df['day']=df['date'].dt.day
        df['minute']=df['date'].dt.minute
        df['hour']=df['date'].dt.hour
        df['day_name']=df['date'].dt.day_name()
        df['only_date']=df['date'].dt.date
        df['month_num']=df['date'].dt.month
        p=[]
        for hour in df[['day_name','hour']]['hour']:
            if hour==23:
                p.append(str(hour)+'-'+str('00'))
            elif(hour==0):
                p.append(str('00'+'-'+str(hour+1)))
            else:
                p.append(str(hour)+'-'+str(hour+1))
        df['peroid']=p

        return df
except Exception as e :
    print(e)
    # file=open('WhatsApp Chat with State Line.txt','r',encoding='utf-8')
    # data=file.read()
    # get_data(data)