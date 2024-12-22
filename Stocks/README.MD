# Stock Sentiment Analyzer

The **Stock Sentiment Analyzer** is a Python tool that performs stock price and news sentiment analysis. The tool fetches stock prices, analyzes news headlines using NLTK's VADER sentiment analysis, visualizes stock price trends, and sends automated email alerts for significant changes in stock prices. It's ideal for monitoring market trends and understanding how news sentiment can impact stock performance.

## Features

- Fetches stock prices using an API (e.g., Yahoo Finance).
- Analyzes news headlines sentiment using NLTK's VADER.
- Visualizes stock price trends with `matplotlib`.
- Sends automated email alerts on significant stock price movements.

## Installation

### 1. Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/BinaryBrilliance8/stock-sentiment-analyzer.git
cd stock-sentiment-analyzer
### 2.Install the required Python packages:
pip install -r requirements.txt
import nltk
### 3.Download the VADER lexicon:
nltk.download('vader_lexicon')
### 4.Run the script:
python stock_sentiment_analyzer.py


