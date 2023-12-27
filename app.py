import matplotlib.pyplot as plt
import streamlit as st
import main,helper
import seaborn as sns
# Content for the main area
st.title(" Chat Anylisis ")
st.write("This is the main content of your Streamlit app.")
# Custom CSS styling for the sidebar

# Sidebar content
try:
    st.sidebar.title("File Upload Only text format")

    upload_file=st.sidebar.file_uploader("Upload your file here")
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        data=bytes_data.decode('utf-8')
        df=main.get_data(data)
        

        #NOTE -  fetch unique user 
        user_list =df['user'].unique().tolist() #REVIEW - tolist() is used to convert a NumPy array to a regular Python list.
        
        
        
        for user in user_list:
            if user=='group_noitfication':
                
                user_list.remove('group_noitfication')
    
        user_list.sort()
        # st.sidebar.write("Select User")
        user_list.insert(0,'All')
        selected_user=st.sidebar.selectbox("Select User",user_list)
        if st.sidebar.button("Show Analysis"):
            #STUB - showing the devloper name =
            st.markdown(
            """<div style="position: fixed; bottom: 10px; right: 10px; text-align: right; font-style: italic;">
            Devlop By Nitin kumar
            </div>""",
            unsafe_allow_html=True)
            #========================

            #NOTE -  showing stats in ui 
            col1,col2,col3,col4 =st.columns(4) #REVIEW - Creates one or more side-by-side columns for displaying elements like text, images, and other widgets.
            total_meassge,total_words,total_media,total_link=helper.fetch_stats(selected_user,df)
            with col1:
                st.header('Total Messages')
                st.title(total_meassge)
            with col2:
                st.header('Total Words')
                st.title(total_words) 
            with col3:
                st.header('Total Media')
                st.title(total_media) 
            with col4:
                st.header('Total Links')
                st.title(total_link) 
            #NOTE - ============ monthlytime line =======================================================
            st.title("Monthly Timeline")
            time = helper.monthly_time(selected_user, df)
            time['color'] = time['message'].apply(lambda x: '#7D3C98' if x == min(time['message']) else ('#FF5733' if x == max(time['message']) else '#1F618D'))
            fig, ax = plt.subplots()
            ax.scatter(time['time'], time['message'],color =time['color'])
            ax.set_xlabel('Months')
            ax.set_ylabel('Total message')
            plt.xticks(rotation='vertical')
            # Display the plot in Streamlit
            st.pyplot(fig)

            #NOTE - =============== daly time line ==========================================================
            st.title('Daly Timeline')
            daly = helper.daliy_timeline(selected_user, df)
            daly['color'] = daly['message'].apply(lambda x: '#1C2833' if x == min(daly['message']) else ('#5B2C6F ' if x == max(daly['message']) else '#0E6655'))
            fig, ax = plt.subplots()
            ax.scatter(daly['only_date'], daly['message'],color ='red')
            ax.set_ylabel('Total Message')
            ax.set_xlabel(' Days')
            plt.xticks(rotation='vertical')
            # Display the plot in Streamlit
            st.pyplot(fig)
            #NOTE -========================= weakly meassges================
            weak_ms=helper.weakly_timeline(selected_user,df)
            st.title("Active Map")
            col1,col2=st.columns(2)
            with col1:
                weak_ms=helper.weakly_timeline(selected_user,df)
                st.header('Most busy day')
                fig,ax=plt.subplots()
                ax.bar(weak_ms.index,weak_ms.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                weak_ms=helper.month_active(selected_user,df)
                st.header('Most busy month')
                fig,ax=plt.subplots()
                ax.bar(weak_ms.index,weak_ms.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            #NOTE - =========================================
            st.title('Weekly Activity Map')
            het_map=helper.Active_hetmsp(selected_user,df)
            custom_cmap = 'coolwarm'
            # Create the heatmap
            fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size if needed
            heatmap = sns.heatmap(het_map, cmap=custom_cmap, annot=True, fmt="g", linewidths=.5, cbar_kws={'label': 'Message Count'})
            # Set labels and title
            plt.xlabel('Period')
            plt.ylabel('Day Name')
            plt.title('Weekly Activity Map')
            # Add colorbar
            cbar = heatmap.collections[0].colorbar
            cbar.set_label('Message Count', rotation=270, labelpad=15)
            # Show the plot using Streamlit
            st.pyplot(fig)

            



            #NOTE -  finding the bususet user in the group (group level)
            if selected_user =='All':
                st.title('Most Busy Users')
                x,per=helper.fetch_busy(df)
                fig,ax =plt.subplots()
                col1, col2=st.columns(2)
                with col1:
                    ax.bar(x.index,x.values,color= 'Red')
                    ax.bar(x.index,x.values)
                    st.pyplot(fig)

                with col2:
                    st.dataframe(per)

            #NOTE -  World cloud
            st.title("World Cloud")
            world_Cloud=helper.Creates_wordcloud(selected_user,df)
            fig,ax=plt.subplots()
            ax.imshow(world_Cloud) 
            st.pyplot(fig)
            #NOTE -  Most comman words
            
            st.title('Most comman Messages')
            most_word_df =helper.most_common_words(selected_user,df)
            most_word_df['color'] = most_word_df[1].apply(lambda x: '#DC7633' if x == min(most_word_df[1]) else ('#7D3C98' if x == max(most_word_df[1]) else '#DAF7A6'))
            fig, ax = plt.subplots()
            ax.barh(most_word_df[0], most_word_df[1],color=most_word_df['color'])
            plt.style.use('fivethirtyeight')
            ax.set(xlabel='Total Count', ylabel='Total Messages',
        title='Most comman Messages')
            st.pyplot(fig)
        #NOTE - ===================== Emoji anayliss=====================
            st.title('Emoji Analysis ')
            em_df=helper.Emoji_helper(selected_user,df)
            col1, col2=st.columns(2)
            with col1:
                # Transpose the DataFrame
                em_df_transposed = em_df.T
                table_height = 300
                # Display the transposed table
                st.table(em_df_transposed.head(40))
            
            print(em_df[1])
            em_df['color'] = em_df[1].apply(lambda x: 'red' if x == min(em_df[1]) else ('green' if x == max(em_df[1]) else 'yellow'))
            fig, ax = plt.subplots(figsize=(40,35))
            bars = ax.bar(em_df[0], em_df[1], color=em_df['color'])
            ax.bar(em_df[0], em_df[1], color=em_df['color'])
            ax.set_xlabel('Emoji', fontsize=80)
            ax.set_ylabel('Count', fontsize=80)
            ax.set_title(f'Emoji  Analysis for {selected_user}',fontsize=100)
            ax.set_xticks(em_df[0])    
            ax.tick_params(axis='x', rotation=45, labelsize=25)
            ax.tick_params(axis='y', labelsize=25)
            plt.tight_layout()
            st.pyplot(fig)
except Exception as e:
    # Display an error message
    st.error(f"An error occurred: {e}",icon="🚨")



            
            

                
                
                
                