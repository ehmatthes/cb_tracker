# Terminal tracker for coinbase
#
# This script is a simple, minimalist terminal-based ticker for 
#  coinbase.com.
#
# It was written to let me keep an eye on the price at coinbase
#  without having to keep a browser tab open. It is not meant to
#  facilitate buying or selling, or doing anything with anyone's
#  personal account.
#
# It does not keep any historical data; it is just written to let 
#  you watch price movement from the time you start running the 
#  script.
#
# I am mostly interested in knowing when the price is just above
#  local minima, so it reports the amount above the low price.
# 
# The output is formatted to fit nicely in a thin terminal window on
#  the side of the screen.

# Output:
#
#  timestamp - price
#  timestamp - price
#  ...
#
#  high:       price
#  low:        price
#  difference: amount
#
#  current:    price
#  #(commented out) above low:  amount
#  below high: amount

# Parameters
#
#  INTERVAL: how often to poll coinbase, default 60 seconds
#  MAX_DISPLAY: how many prices to show, default 25
#  MAX_PRICES: how many prices to keep, default 10000; 
#    affects calculation of high/ low, other stats
#  DEBUG: when True, INTERVAL=1 second, MAX_DISPLAY=5

# Questions, comments: @ehmatthes

import os
import requests, json
from time import sleep
from datetime import datetime

# Coinbase API url that should give something between the buy and
#  sell price, updated every few seconds.
price_url = 'https://coinbase.com/api/v1/prices/spot_rate'

# Parameters
INTERVAL = 60
MAX_PRICES = 1000
MAX_DISPLAY = 25
DEBUG = False

# prices=[{'timestamp': ts, 'price': price}, ...]
prices = []

if DEBUG:
    INTERVAL = 1
    MAX_DISPLAY = 5


def get_price():
    # Gets current price at coinbase. Stores in prices, with timestamp.
    # Price is something between buy and sell price, updated
    #  every few seconds.
    try:
        r = requests.get(price_url)
    except:
        # Couldn't get price; no error reporting at this point.
        pass
    if r.status_code == 200:
        data = json.loads(r.text)
        price = float(data['amount'])
        timestamp = datetime.now()
        prices.append({'timestamp': timestamp, 'price': price})


def get_min_max():
    # One trillion, in honor of tothemoonguy
    min = 1000000000
    min_ts = datetime.now()
    max = 0
    max_ts = datetime.now()

    for price_dict in prices:
        if float(price_dict['price']) < min:
            min = round(price_dict['price'], 2)
            min_ts = price_dict['timestamp']
        elif float(price_dict['price']) > max:
            max = round(price_dict['price'], 2)
            max_ts = price_dict['timestamp']

    return(min, min_ts, max, max_ts)


def show_single_price(price_dict, index):
    # Shows the price associated with a given time.
    timestamp = price_dict['timestamp'].strftime("%H:%M:%S")
    price = "{0:.2f}".format(price_dict['price'])
    if index == 0:
        print('$ %s - %s' % (price, timestamp))
    else:
        print('  %s - %s' % (price, timestamp))


def display_info():
    # Clears the terminal window, and shows all relevant info.
    os.system('clear')
    print("Current coinbase price data:")
    if len(prices) > MAX_DISPLAY:
        for index, price_dict in enumerate(prices[-MAX_DISPLAY:]):
            show_single_price(price_dict, index)
    else:
        for index, price_dict in enumerate(prices):
            show_single_price(price_dict, index)
    print("\n")
    
    min_price, min_ts, max_price, max_ts = get_min_max()
    difference = "{0:.2f}".format(max_price - min_price)
    current_price = prices[-1]['price']
    above_low = "{0:.2f}".format(current_price - min_price)
    below_high = "{0:.2f}".format(max_price - current_price)
    min_price = "{0:.2f}".format(min_price)
    max_price = "{0:.2f}".format(max_price)
    current_price = "{0:.2f}".format(current_price)

    print("high:       $ %s - %s" % (max_price, max_ts.strftime("%H:%M:%S")))
    print("low:          %s - %s" % (min_price, min_ts.strftime("%H:%M:%S")))
    print("difference:  ", difference)
    print("\n")
    print("current:    $", current_price)
    #print("above low:   ", above_low)
    print("below high:  ", below_high)

while True:
    # Get price.
    get_price()

    # Make sure prices does not grow too large.
    if len(prices) > MAX_PRICES:
        prices.pop(0)

    # Show updated information.
    display_info()

    # Pause before grabbing next price.
    sleep(INTERVAL)
