# This code scrapes the symbols for both the FTSE 100 and S&P 100 companies
# It then scrapes each company's data, and compares the most recent price with
# the price at the start of 2008. It saves the ratio of these prices.

################################################################################
################################################################################

import urllib2
import matplotlib.pyplot as plt
import datetime
import numpy as np
import seaborn as sns	# seaborn is used to make nice plots. Not 100% necessary.
sns.set()

# function to get data for each symbol
def get_data(ticker):
    try:
        url1 = "http://chart.finance.yahoo.com/table.csv?s=" + ticker + "&a=1&b=1&c=1970&d=10&e=22&f=2016&g=d&ignore=.csv"
        html1 = urllib2.urlopen(url1).read()

        data = html1.split("\n")
        dates, closing = [], []

        for i in data[1:-1]:
            datestring = i.split(",")[0]
            dates.append(datetime.datetime(int(datestring[:4]), int(datestring[5:7]), int(datestring[8:])))
            closing.append(float(i.split(",")[-1]))

        if dates[-1] > datetime.datetime(2008, 1, 1):
			# if the time-series ends before 2008, return 99999.
            return ticker, 999999.

        for index, value in enumerate(dates):
            if value < datetime.datetime(2008, 1, 1):
                break

        return ticker, closing[0]/closing[index]

    except:
        return ticker, 999999.    

################################################################################
# Scraping the FTSE tickers

tickers = []
for page_numb in ["0", "1", "2"]:
    url2 = "https://uk.finance.yahoo.com/q/cp?s=%5EFTSE&c=" + page_numb
    html2 = urllib2.urlopen(url2).readlines()

    for line in html2:
        if 'COMPONENTS FOR ^FTSE' in line:
            break

    data = line.split('<a href="/q?s=')


    for i in data[1:]:
        tickers.append(i.split('">')[0])


# Use FTSE tickers to get each company data
names, returns = [], []
for symbol in tickers:
    name, returnz = get_data(symbol)
    print symbol, returnz
    if returnz != 999999.:
        names.append(name)
        returns.append(returnz)



# Sort the lists by the returns
returns, names = (list(x) for x in zip(*sorted(zip(returns, names), key=lambda pair: pair[0])))

################################################################################
# Scraping the S&P 100 tickers
from bs4 import BeautifulSoup	# used for webscraping

tickers2 = []

url2 = "https://en.wikipedia.org/wiki/S%26P_100"
html2 = urllib2.urlopen(url2).read()

soup = BeautifulSoup(html2)
tables = soup.find_all('table')

for row in tables[1].findAll('tr')[1:-1]:
	col = row.findAll('td')
	tickers2.append(str(col[0].text))


# Use S&P tickers to get each company data
names2, returns2 = [], []
for symbol in tickers2:
    name2, returnz2 = get_data(symbol)
    print symbol, returnz2
    if returnz2 != 999999.:
        names2.append(name2)
        returns2.append(returnz2)


# Sort the lists by the returns
returns2, names2 = (list(x) for x in zip(*sorted(zip(returns2, names2), key=lambda pair: pair[0])))

################################################################################
# Plotting the Data!

# get the data for the actual FTSE100 index, just for comparison
FTSE_name, FTSE_value = get_data("^FTSE")

# make a plot with two subplots
fig = plt.figure(1)
plt.clf()
ax = plt.subplot(211)

xlist = np.arange(len(returns))	# list for x-axis (1 -> len(returns))
plt.plot(xlist, returns, 'ok')

# Annotate company names
for index, value in enumerate(xlist):
    x1, y1 = xlist[index], returns[index]
    changey = [2, -1, 1, -2][index%4]     

	# plot the company names with arrows to the company points
    ax.annotate(names[index], xy=(x1, y1), xytext=(x1, y1 + changey), 
                horizontalalignment = 'center', fontsize = 15,
                arrowprops=dict(headwidth = 0.1, width = 0.0))

# plot a line for the FTSE100 index to compare to individual companies
plt.axhline(FTSE_value, linestyle = "dashed")

plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
plt.tick_params(axis='both', which='major', labelsize=20)

plt.xlim([-2, 93])
plt.ylim([-2, 25])

plt.title("FTSE 100 Company Returns since 01-01-2008", fontsize = 24)
plt.ylabel("Return", fontsize = 24)

################################################################################
# Same as above, except for S&P 100
ax = plt.subplot(212)

xlist2 = np.arange(len(returns2))
plt.plot(xlist2, returns2, 'ok')

# Annotate company names
for index, value in enumerate(xlist2):
    x1, y1 = xlist2[index], returns2[index]
    changey = [2, -1, 1, -2][index%4]     

    ax.annotate(names2[index], xy=(x1, y1), xytext=(x1, y1 + changey), 
                horizontalalignment = 'center', fontsize = 15,
                arrowprops=dict(headwidth = 0.1, width = 0.0))


plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
plt.tick_params(axis='both', which='major', labelsize=20)

plt.xlim([-2, 93])
plt.ylim([-2, 25])

plt.title("S&P 100 Company Returns since 01-01-2008", fontsize = 24)
plt.ylabel("Return", fontsize = 24)
plt.show()
