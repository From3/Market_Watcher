# -*- coding: utf-8 -*-

import yfinance as yf
import datetime as dt
import smtplib
from time import sleep
from os import environ

EMAIL_USER = environ["EMAIL_USER"]
EMAIL_PASSWORD = environ["EMAIL_PASSWORD"]
EMAIL_RECEIVER = environ["EMAIL_RECEIVER"]

SMTP_SERVER = "smtp.gmail.com"
EMAIL_PORT = 587


def send_email(subject, body):
    with smtplib.SMTP(SMTP_SERVER, EMAIL_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        
        msg = f"Subject: {subject}\n\n{body}"
        
        smtp.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg)


def email_manager(previous_triggers, current_triggers):
    previous_triggers = previous_triggers.keys()
    new_triggers = tuple(set(current_triggers.keys()).difference(previous_triggers))
    new_triggers_len = len(new_triggers)
    
    if new_triggers_len < 1:
        return
    elif 0 < new_triggers_len < 3:
        subject = " and ".join(new_triggers)
    else:
        subject = "Multiple tickers"
    
    body = ""
    for trigger in new_triggers:
        body += f"{trigger}\n" # Write down what will be included in the body of email
    
    send_email(subject + " reached threshold", body)


def rsi(df, n=14):
    """ Relative strength index
    Signals if overbought or oversold, overbought = value > 70, oversold = value < 30"""
    df = df.copy()
    df["Change"] = df["Adj Close"] - df["Adj Close"].shift(1)
    df["Gain"] = np.where(df["Change"] >= 0, df["Change"], 0)
    df["Loss"] = np.where(df["Change"] < 0, -1 * df["Change"], 0)
    df["Avg Gain"] = df["Gain"].ewm(alpha=1 / n, min_periods=n).mean()
    df["Avg Loss"] = df["Loss"].ewm(alpha=1 / n, min_periods=n).mean()
    df["RS"] = df["Avg Gain"] / df["Avg Loss"]
    return 100 - (100 / (1 + df["RS"]))


def main(tickers):
    ohlcv_data = {}
    triggers = {}
    
    start_date = dt.datetime.today() - dt.timedelta(90)
    end_date = dt.datetime.today()
    
    for ticker in tickers:
        try:
            ohlcv_data[ticker] = yf.download(ticker, start_date, end_date, interval="1d")
            ohlcv_data[ticker].dropna(how="all", inplace=True)
        except:
            print(f"[ERROR] Can't reach \"{ticker}\" data")
            
    for ticker in tickers:
        # Insert requested indicators here
        
        # Insert requested trigger conditions here which will create a new key (ticker) and value (information which should be passed to 'triggers' dictionary)
    
    return triggers


if __name__ == "__main__":
    
    previous_triggers = {}
    
    while True:
        tickers = () # Write down required tickers within the tuple
        current_triggers = main(tickers)
        email_manager(previous_triggers, current_triggers)
        previous_triggers = current_triggers
        sleep(300) # This watcher will run every 5 minutes
