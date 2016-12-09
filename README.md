# FTSE100_returns
Python script to scrape FTSE100 and S&P100 data.

![figure_1](https://cloud.githubusercontent.com/assets/20742138/21055608/094840ac-be2a-11e6-8f6e-a6d0cc76a1a9.png)


Scrapes the symbol for each company in the FTSE100 from here:

https://uk.finance.yahoo.com/q/cp?s=%5EFTSE

And the S&P 100 from the wikipedia page:

https://en.wikipedia.org/wiki/S%26P_100

For each company, it then goes to Yahoo Historical, and downloads their time-series. It compares the most recent closing price with the price on the 1st of January 2008. 

Finally, it ranks the companies and plots them.

Ashtead Group plc turns out to be the winner, from the FTSE100, with a return of over 2100%...

The S&P100 winner turns out to be The Priceline Group, with a return of 1300%.
