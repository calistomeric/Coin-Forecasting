import streamlit as st
import pandas as pd
import tweepy
import pymongo
from textblob import TextBlob
import re

API_Key =  'IPIMavVwaN13mt4s6vZwXnXWm'
API_Key_Secret = 'mx8GDMlpBAYA8Le0uWE59hdcvnPTfqYjrJqRZ9jLz4RyBCHZ9c'
Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAJJycQEAAAAAuumt%2FjnE7YLpLSul2LoqabbNxTQ%3DSVkzWnsMs00Ps41l9pxuvhMtynzZw9BPDamVuyIdpPNnPDch3H'
Access_Token =  '1489332332498726917-dZ9eyJFy7lqQDNkjIA5mEoNUjyNu7t'
Access_Token_Secret =  'm6w9jehIf5k4qWajRD6YWcb8NDqUylOgJ6xTmLAeH7cz2'

auth = tweepy.OAuthHandler(API_Key, API_Key_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


# "mongodb+srv://calistus:calistus@cluster0.m97pu3i.mongodb.net/?retryWrites=true&w=majority"
mongo_client = pymongo.MongoClient("mongodb+srv://burlacuemilia07:root@dbdisertatie.syso6he.mongodb.net/?retryrites=true&w=majority")
# mongo_client = pymongo.MongoClient("mongodb+srv://calistus:calistus@cluster0.m97pu3i.mongodb.net/?retryWrites=true&w=majority")
client = tweepy.Client(bearer_token=Bearer_Token, wait_on_rate_limit=True)
db = mongo_client['DBdisertatie']
# db = mongo_client['StoreTweet']

def get_tweet(start, end, search_term, limit):
    #####################################################
    # client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAJJycQEAAAAAuumt%2FjnE7YLpLSul2LoqabbNxTQ%3DSVkzWnsMs00Ps41l9pxuvhMtynzZw9BPDamVuyIdpPNnPDch3H', wait_on_rate_limit=True)

    store_tweets = []

    tweets = tweepy.Paginator(client.search_recent_tweets, query=search_term,
                            tweet_fields= ['created_at', 'lang', 'id', 'text', 'public_metrics'], 
                            start_time = start, 
                            end_time = end, max_results=100).flatten(limit=limit)

            
    for i, tweet in enumerate(tweets):
        if i >= limit:
            break
        tweet_dict = {
            'tweet_date':tweet.created_at,
            'language': tweet.lang,
            'id':tweet.id,
            'tweet':tweet.text, 
            'reply_count':list(tweet.public_metrics.values())[1],
            'retweet_count':list(tweet.public_metrics.values())[0],
            'like_count':list(tweet.public_metrics.values())[2]
        }
        store_tweets.append(tweet_dict)
    data = pd.DataFrame(store_tweets)
    return data

def main():
        ########## setup of mainpage  #################

    st.markdown(f"<h1 style = 'text-align: center; background-color:orangered'>Crypto Signal</h1>", unsafe_allow_html=True)
    st.text('')
    st.markdown(
        """<style>
    div > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px;
        font-weight: bold;
        font-family: Serif
    }
        </style>
        """, unsafe_allow_html=True)
    
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: lightblue;
    }
    </style>""", unsafe_allow_html=True)
    
    
    search_term = st.sidebar.text_input('Coin Name\n', key='input_key_1')
    
    #################################### 
    
    start = st.sidebar.text_input('Start date', key = 'start_key')
    if start:
        start = start + 'T00:00:00Z'
    end = st.sidebar.text_input('End Date', key='end_key')
    if end:
        end = end + 'T00:00:00Z'

    # sets limit of slider
    limit = st.sidebar.slider('\nNo of Tweets\n', 1, 1000, value = 1, key='limit_slider')
    if limit:
        limit = limit

    ########### right page ############
    st.title('Tweets', 'main_title')
    try:
        if st.button('Scrape Tweet', key='scrape_button_key'):
            data = get_tweet(start, end, search_term, limit)
            st.write('Scraping {} tweets ...'.format(search_term))
            st.write(data)
            
    
        if st.button('Upload to MongoDB', key='upload_button_key'):
            data = get_tweet(start, end, search_term, limit)
            db[search_term].insert_many(data.to_dict('records'))
            css_temp = f"""
            <p style='background-color:tomato; border-radius:7px; padding:10px; color:white; text-align:center;
            font-size: 18px'>{len(data)} Tweets successfully uploaded to MongoDB</style><BR>
            </p>
            """
            st.markdown(css_temp, unsafe_allow_html=True)

        if st.button('Predict', key='predict_button_key'):
            data = get_tweet(start, end, search_term, limit)
            def cleanText(text):
                text = re.sub('@[A-Za-z0-9_]+', '', text) #removes @mentions
                text = re.sub('#','', text) #removes hastag '#' symbol
                text = re.sub('RT[\s]+','',text) # removes retweets symbol
                text = re.sub('https?:\/\/.*[\r\n]*', '', text) # removes various characters
                return text
            
            #get subjectivity and polarity of tweets with a function
            def getSubjectivity(text):
                return TextBlob(text).sentiment.subjectivity
            
            #get polarity with a function
            def getPolarity(text):
                return TextBlob(text).sentiment.polarity
            
            #create a function to check negative, neutral and positive analysis
            def getAnalysis(score):
                if score < 0:
                    return 'Negative'
                elif score == 0:
                    return 'Neutral'
                else:
                    return 'Positive'

            data['CleanedTweet'] = data['tweet'].apply(cleanText)
            data['Subjectivity'] = data['CleanedTweet'].apply(getSubjectivity)
            data['Polarity'] = data['CleanedTweet'].apply(getPolarity)
            data['Analysis'] = data['Polarity'].apply(getAnalysis)

            if data[data['Analysis']=='Positive']['Analysis'].count() > data[data['Analysis']=='Negative']['Analysis'].count():
                css_temp = f"""
                <p style='background-color:tomato; border-radius:7px; padding:10px; color:white; text-align:center;
                font-size: 18px; foreground-color:green'>BUY {search_term}</style><BR>
                </p>
                """
                st.markdown(css_temp, unsafe_allow_html=True)
            else: 
                css_temp = f"""
                <p style='background-color:tomato; border-radius:7px; padding:10px; color:white; text-align:center;
                font-size: 18px', foreground=color: red>SELL {search_term}</style><BR>
                </p>
                """
                st.markdown(css_temp, unsafe_allow_html=True)
            
    except (ValueError):
        pass


if __name__=='__main__':
    main()
