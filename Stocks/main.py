import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
import smtplib

# Download VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Stock and news configuration
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Store your API keys securely
STOCK_API_KEY = "OH16VSS0X5ZUZQM0."
NEWS_API_KEY = "3c5e4b41946947beab712943dd0b1f52"


# Step 1: Fetch stock prices for yesterday and day before yesterday
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# Calculate price difference and percentage change
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = "🔺" if difference > 0 else "🔻"
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

# Step 2: Fetch news articles if price change exceeds a certain threshold
if abs(diff_percent) > 1:  # Adjust percentage threshold as needed
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"][:10]  # Get top 3 articles

    # Step 3: Sentiment analysis on news articles
    sia = SentimentIntensityAnalyzer()
    for article in articles:
        # Handle case where description might be None
        headline_sentiment = sia.polarity_scores(article["title"])
        description_sentiment = sia.polarity_scores(article["description"]) if article["description"] else None
        print(f"Headline Sentiment: {headline_sentiment}")
        print(f"Description Sentiment: {description_sentiment}")

# Step 4: Plot stock prices for the last 7 days
dates = [key for key in data.keys()]
closing_prices = [float(data[date]["4. close"]) for date in dates[:7]]

plt.plot(dates[:7], closing_prices)
plt.title(f"{STOCK_NAME} Closing Prices - Last 7 Days")
plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")
plt.xticks(rotation=45)
plt.show()

# Step 5: Send a daily email summary
def send_email(subject, body):
    my_email = "dummee18@gmail.com"
    password = "dfdqjrtfjldglbbw"  # Ensure your password is stored securely, e.g., environment variables
    
    with smtplib.SMTP("smtp.gmail.com",587, timeout=30) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="dummeee18@yahoo.com",
            msg=f"Subject: {subject}\n\n{body}".encode('utf-8')
        )

# Send email if there's a significant stock price change
if abs(diff_percent) > 1:
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description'] or 'No description available.'}" for article in articles]
    email_subject = f"{STOCK_NAME} Daily Summary"
    email_body = "\n".join(formatted_articles)
    send_email(email_subject, email_body)
    
'''import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file (you need to create a .env file)
load_dotenv()

# Download VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Stock and news configuration
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Store your API keys in environment variables for security
STOCK_API_KEY = os.getenv("OH16VSS0X5ZUZQM0.")
NEWS_API_KEY = os.getenv("3c5e4b41946947beab712943dd0b1f52")
EMAIL_PASSWORD = os.getenv("dfdqjrtfjldglbbw")

# Step 1: Fetch stock prices for yesterday and the day before
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

try:
    stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
    stock_response.raise_for_status()  # Check for request errors
    stock_data = stock_response.json().get("Time Series (Daily)", {})
    if not stock_data:
        raise ValueError("No stock data found")

    data_list = [value for (key, value) in stock_data.items()]
    yesterday_data = data_list[0]
    day_before_yesterday_data = data_list[1]

    yesterday_closing_price = yesterday_data["4. close"]
    day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

    # Calculate price difference and percentage change
    difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
    up_down = "🔺" if difference > 0 else "🔻"
    diff_percent = round((difference / float(yesterday_closing_price)) * 100)

except (requests.exceptions.RequestException, IndexError, KeyError, ValueError) as e:
    print(f"Error fetching or processing stock data: {e}")
    stock_data = {}

# Step 2: Fetch news articles if price change exceeds a threshold
if stock_data and abs(diff_percent) > 1:  # Adjust percentage threshold as needed
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    try:
        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        news_response.raise_for_status()
        articles = news_response.json().get("articles", [])[:3]  # Get top 3 articles

        if not articles:
            raise ValueError("No news articles found")

        # Step 3: Sentiment analysis on news articles
        sia = SentimentIntensityAnalyzer()
        for article in articles:
            headline_sentiment = sia.polarity_scores(article["title"])
            description_sentiment = sia.polarity_scores(article["description"]) if article["description"] else None
            print(f"Headline Sentiment: {headline_sentiment}")
            print(f"Description Sentiment: {description_sentiment}")

    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching or processing news data: {e}")

# Step 4: Plot stock prices for the last 7 days
if stock_data:
    try:
        dates = [key for key in stock_data.keys()]
        closing_prices = [float(stock_data[date]["4. close"]) for date in dates[:7]]

        plt.plot(dates[:7], closing_prices)
        plt.title(f"{STOCK_NAME} Closing Prices - Last 7 Days")
        plt.xlabel("Date")
        plt.ylabel("Closing Price (USD)")
        plt.xticks(rotation=45)
        plt.tight_layout()  # Ensure the labels don't overlap
        plt.show()
    except (IndexError, KeyError) as e:
        print(f"Error plotting stock data: {e}")

# Step 5: Send a daily email summary
def send_email(subject, body):
    my_email = "dummee18@gmail.com"
    password = EMAIL_PASSWORD  # Store securely in environment variables

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="dummeee18@yahoo.com",
                msg=f"Subject: {subject}\n\n{body}".encode('utf-8')
            )
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

# Send email if there's a significant stock price change
if stock_data and abs(diff_percent) > 1:
    try:
        formatted_articles = [
            f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description'] or 'No description available.'}"
            for article in articles
        ]
        email_subject = f"{STOCK_NAME} Daily Summary"
        email_body = "\n".join(formatted_articles)
        send_email(email_subject, email_body)
    except KeyError:
        print("Error preparing email content")'''











