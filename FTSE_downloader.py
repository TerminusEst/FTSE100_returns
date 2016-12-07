import urllib2
import matplotlib.pyplot as plt
import datetime
import numpy as np
import seaborn as sns
sns.set()

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
    print symbol
    name, returnz = get_data(symbol)
    if returnz != 999999.:
        names.append(name)
        returns.append(returnz)



# Sort the lists by the returns
returns, names = (list(x) for x in zip(*sorted(zip(returns, names), key=lambda pair: pair[0])))


################################################################################
# Plotting the Data!

FTSE_name, FTSE_value = get_data("^FTSE")


fig = plt.figure(1)
plt.clf()
ax = plt.subplot(111)

xlist = np.arange(len(returns))
plt.plot(xlist, returns, 'ok')

# Annotate company names
for index, value in enumerate(xlist):
    x1, y1 = xlist[index], returns[index]
    changey = [1.5, -0.75, 0.75, -1.5][index%4]     

    ax.annotate(names[index], xy=(x1, y1), xytext=(x1, y1 + changey), 
                horizontalalignment = 'center', fontsize = 15,
                arrowprops=dict(headwidth = 0.1, width = 0.0))

plt.axhline(FTSE_value, linestyle = "dashed")

plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
plt.tick_params(axis='both', which='major', labelsize=20)

plt.xlim([-2, 93])
plt.ylim([-2, 25])

plt.title("FTSE 100 Company Returns since 01-01-2008", fontsize = 24)
plt.ylabel("Return", fontsize = 24)
plt.show()




























































