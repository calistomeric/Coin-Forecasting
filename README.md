# Coin-Forecasting
This app helps people to decide when to buy or sell a particular crypto coin based on twitter sentiments. It scrapes tweets and extracts the sentiment of the tweets on a particular coin or token e.g bitocoin and then gives a buy signal if positive sentiment is greater than negative sentiment or sell signal if negative sentiment is greater than positive sentiment. The app was developed using streamlit app and deployed on streamlit cloud. To use the app you have to enter your bearer token and your MongoDB database name.
The app contains the following inputs:
1. **Coin Name**: This accepts the name of the coin you want to scrape tweets about. If you want to scrape tweets about bitcoin simply enter bicoin.
2. **Start Date**: This contains the date from which you want to start scraping the tweet. This should not be more than 7 days from the present date. The format for the date is yyyy-mm-dd.
3. **End Date**: This contains the date you want to end the tweet scraping. All other information applies as **Start Date**.
4. **No of Tweets**: This contains the number of tweets you want to scrape. The option is presented in the form of a sliding scale with a limit of 1000 tweets.

## How to Use
1. Fill and choose the appropriate option as highlighted above.
2. Click on **Scrape Tweet** button in order to start scraping the tweets. As the tweets are scraped they will be displayed on the interface.
3. Click on **Upload to MongoDB** button in order to upload the scraped tweets to MongoDB.
4. Click on **Predict** button in order to display the prediction. Buy is displayed if positive sentiments is greater than negative sentiments while sell is displayed if negative sentiments is greater than positive sentiments.
![Screenshot (5)](https://github.com/calistomeric/Coin-Forecasting/assets/99477055/138ad265-110e-4274-8fe9-31bfadedec0c)
[Click here to use the app](https://calistomeric-coin-forecasting-coin-forecast-1g63bn.streamlit.app/)
