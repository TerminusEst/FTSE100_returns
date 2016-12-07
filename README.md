# FTSE100_returns
Python script to scrape FTSE100 data.

![figure_1](https://cloud.githubusercontent.com/assets/20742138/20985423/5ba76306-bcbc-11e6-9c6b-ce1339064463.png)
The dashed blue line is the return of the FTSE100 index itself.

Scrapes the symbol for each company in the FTSE100 from here:

https://uk.finance.yahoo.com/q/cp?s=%5EFTSE

For each company, it then goes to Yahoo Historical, and downloads their time-series. It compares the most recent closing price with the price on the 1st of January 2008. 

Finally, it ranks the companies and plots them.

Ashtead Group plc turns out to be the winner, with a return of over 2100%...
