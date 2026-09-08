import yfinance as yf
import pandas as pd

def search_company(query):
    search = yf.Search(
        query,
        max_results=8,
        news_count=0
    )

    results = []

    for quote in search.quotes:
        if quote.get("quoteType") == "EQUITY":
            results.append({
                "symbol": quote.get("symbol"),
                "name": quote.get("longname") or quote.get("shortname"),
                "exchange": quote.get("exchange"),
            })

    return results

def get_stock_data(ticker,period):
    data = yf.download(
        ticker,
        period = period,
        interval = "1d",
        auto_adjust = False 
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data

def calculate_basic_statistics(data):
    print("Data rows:", len(data))
    current_price = data["Close"].iloc[-1]
    starting_price = data["Close"].iloc[0]

    highest_price = data["High"].max()
    lowest_price = data["High"].min()

    total_return = (
        (current_price - starting_price)/starting_price
    )*100

    daily_returns = data["Close"].pct_change().dropna()
    average_daily_return = daily_returns.mean()*100

    return{
        "current_price":float(current_price),
        "starting_price":float(starting_price),
        "highest_price":float(highest_price),
        "lowest_price":float(lowest_price),
        "total_return":float(total_return),
        "average_daily_return":float(average_daily_return),
    }

def calculate_moving_average(data):
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    data["SMA_50"] = data["Close"].rolling(window=50).mean()
    data["SMA_200"] = data["Close"].rolling(window=200).mean()

    return data

def calculate_returns(data):

    data["daily_return"] = (data["Close"].pct_change() * 100)

    cumulative_return = (data["Close"].iloc[-1] - data["Close"].iloc[0])/(data["Close"].iloc[0])*100

    average_daily_return = data["daily_return"].mean()

    annualized_return = (
        ((data["Close"].iloc[-1]/data["Close"].iloc[0])**(252/len(data)) - 1)*100
    )

    return{
        "cumulative_return":float(cumulative_return),
        "average_daily_return":float(average_daily_return),
        "annualized_return":float(annualized_return),
    }
