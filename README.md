Coinbase tracker
==========

This is a simple, terminal-based ticker for the current price at Coinbase.

This script is a simple, minimalist terminal-based ticker for 
 coinbase.com.

It was written to let me keep an eye on the price at coinbase
 without having to keep a browser tab open. It is not meant to
 facilitate buying or selling, or doing anything with anyone's
 personal account.

It does not keep any historical data; it is just written to let 
 you watch price movement from the time you start running the 
 script.

I am mostly interested in knowing when the price is just above
 local minima, so it reports the amount above the low price.

The output is formatted to fit nicely in a thin terminal window on
 the side of the screen.

Output:

    timestamp - price
    timestamp - price
    ...
    high:       price - timestamp
    low:        price - timestamp
    difference: amount

    current:    price
	 below high: amount

Parameters

- INTERVAL: how often to poll coinbase, default 60 seconds
- MAX_DISPLAY: how many prices to show, default 25
- MAX_PRICES: how many prices to keep, default 10000; 
   affects calculation of high/ low, other stats
- DEBUG: when True, INTERVAL=1 second, MAX_DISPLAY=5

I'm sure it's buggy, and the code is ugly, but it works minimally.

Requirements
---
Requires [requests](http://requests.readthedocs.org/en/latest/), which can be installed through pip:

    pip install requests

Also requires Python 3 to print the output nicely. It will run under Python 2, but the output will be a bit uglier.
