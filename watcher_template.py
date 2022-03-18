# -*- coding: utf-8 -*-

import yfinance as yf
import datetime as dt
import smtplib
from time import sleep
from os import environ

EMAIL_USER = environ["EMAIL_USER"]
EMAIL_PASSWORD = environ["EMAIL_PASSWORD"]
EMAIL_RECEIVER = environ["EMAIL_RECEIVER"]
EMAIL_PORT = 587


def send_email(subject, body):
    with smtplib.SMTP("smtp.gmail.com", EMAIL_PORT) as smtp:
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
        body += f"{trigger}" # Write down what will be included in the body of email
    
    send_email(subject + " reached threshold", body)


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
