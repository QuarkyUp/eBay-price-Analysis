import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import json
import os
import numpy as np
from scipy.stats import norm
import seaborn as sb

IMPORT = True
appid = "EBAY-APP-ID"

baseurl = "http://svcs.ebay.com/services/search/FindingService/v1?"

queryString = [
    "OPERATION-NAME=findCompletedItems&",
    "SERVICE-VERSION=1.13.0&",
    "SECURITY-APPNAME="+appid+"&",
    "RESPONSE-DATA-FORMAT=JSON&",
    "REST-PAYLOAD&",
    "keywords=iphone+6s+16gb&"
]

paginationEntries="paginationInput.entriesPerPage=100&"
paginationPage="paginationInput.pageNumber="

def itemFilter(dateDay, dateMonth):
    return [
        "itemFilter(0).name=Condition&",
        "itemFilter(0).value(0)=2000&",
        "itemFilter(0).value(1)=2500&",
        "itemFilter(0).value(2)=3000&",
        "itemFilter(0).value(3)=4000&",
        "itemFilter(0).value(4)=5000&",
        "itemFilter(0).value(5)=6000&",
        "itemFilter(1).name=SoldItemsOnly&",
        "itemFilter(1).value=true&",
        "itemFilter(2).name=EndTimeFrom&",
        "itemFilter(2).value=2018-0"+str(dateMonth)+"-"+dateDay+"T00:00:01.000Z&",
        "itemFilter(2).name=EndTimeTo&",
        "itemFilter(2).value=2018-0"+str(dateMonth)+"-"+dateDay+"T23:59:59.000Z&",
        "itemFilter(3).name=HideDuplicateItems&",
        "itemFilter(3).value=true&",
        "itemFilter(4).name=ListedIn&",
        "itemFilter(4).value=EBAY-US&"
        "outputSelector(0)=SellerInfo&",
        "outputSelector(1)=listingInfo&"
    ]


def getRequest(pageNumber, dateDay, dateMonth):
    url = baseurl + ''.join(queryString) + ''.join(itemFilter(dateDay, dateMonth)) + paginationEntries + paginationPage + str(pageNumber)
    r = requests.get(url=url)
    return r

def regression(data, polyDegree, key):
    df = pd.DataFrame(data[key])
    df = df[df['price']!=df['price'].max()]
    meanDF = df.groupby('endTime', as_index=False).mean()
    x = np.arange(len(meanDF.endTime))
    fit = np.polyfit(x, meanDF['price'], polyDegree)
    fit_fn = np.poly1d(fit)

    return df, meanDF, x, fit, fit_fn

if __name__ == '__main__':
# DATA SCRAPING
    if not IMPORT:
        dataAggregation = []
        for dateMonth in range(5, 9):
            for dateDay in range(1, 30):
                for pageNumber in range(1, 6):
                    print('Month : {}, Day : {}, Page Number : {}'.format(dateMonth, dateDay, pageNumber))
                    response = None

                    if (dateMonth == 8 and dateDay > 22):
                        continue
                    if (dateMonth == 5 and dateDay < 25):
                        continue
                    if dateDay < 10:
                        response = getRequest(pageNumber, "0"+str(dateDay), dateMonth).json()
                    else:
                        response = getRequest(pageNumber, str(dateDay), dateMonth).json()
                    
                    if 'findCompletedItemsResponse' in response:
                        if 'searchResult' in response['findCompletedItemsResponse'][0]:
                            if 'item' in response['findCompletedItemsResponse'][0]['searchResult'][0]:
                                data = response['findCompletedItemsResponse'][0]['searchResult'][0]['item']
                                dataAggregation.extend(data)
                                
                                if response['findCompletedItemsResponse'][0]['searchResult'][0]['@count'] != '0':
                                    with open(os.path.dirname(__file__) + '\\' + str(dateMonth) + str(dateDay) + str(pageNumber) + 'ebayDump.json', 'w') as fp:
                                        json.dump(data, fp, indent=4)

        with open(os.path.dirname(__file__) + '\\' + 'ebayDump.json', 'w') as fp:
                json.dump(dataAggregation, fp, indent=4)
    else:
        with open(os.path.dirname(__file__) + '\\' + 'ebayDump.json') as fp:
            dataAggregation = json.load(fp)

# DATA CLEANING
    filteredData = []
    for e in dataAggregation:
        item = {
            'title' : e['title'][0],
            'price' : float(e['sellingStatus'][0]['currentPrice'][0]['__value__']),
            'endTime' : e['listingInfo'][0]['endTime'][0].replace('T', ' ')[:-14],
            'condition': e['condition'][0]['conditionDisplayName'][0],
            'sellerUserName': e['sellerInfo'][0]['sellerUserName'][0],
            'feedbackScore': float(e['sellerInfo'][0]['feedbackScore'][0]),
            'positiveFeedbackPercent': float(e['sellerInfo'][0]['positiveFeedbackPercent'][0]),
            'feedbackRatingStar': e['sellerInfo'][0]['feedbackRatingStar'][0]
        }
        filteredData.append(item)
    
# DATA MODELING
    dataArrangedByCondition = {}
    for e in filteredData:
        dataArrangedByCondition.setdefault(e['condition'], []).append(e)

    # Print dataset size
    for key, value in dataArrangedByCondition.items():
        print(key + ' : ' + str(len(value)))

    # Price Histogram
    plt.clf()
    priceHistDF = pd.DataFrame(filteredData)
    priceHistDF = priceHistDF[['price']]
    priceHistDF = priceHistDF[priceHistDF['price'] < 600]
    priceHistDF['price'].plot(kind='hist', density=True, bins=50)
    plt.suptitle('Price Histogram of iPhone 6s 16GB')
    plt.savefig('Histogram Evolution.png')

    # Price per feedbackStore
    plt.clf()
    priceFeedbackDF = pd.DataFrame(filteredData)
    priceFeedbackDF = priceFeedbackDF[['price', 'positiveFeedbackPercent']]
    priceFeedbackDF = priceFeedbackDF[priceFeedbackDF['price'] < 600]
    priceFeedbackDF = priceFeedbackDF[priceFeedbackDF['positiveFeedbackPercent'] > 60]
    priceFeedbackDF.plot(kind='scatter', x='price', y='positiveFeedbackPercent', s=2)
    plt.suptitle('Price Distribution of iPhone 6s 16GB Over Seller\'s Feedback Score')
    plt.savefig('Distribution.png')

    # Price Regression
    # Used
    plt.clf()
    usedDF, meansUsedDF, x, fit, fit_fn = regression(dataArrangedByCondition, 3, 'Used')
    meansUsedDF.plot(x='endTime', y='price', figsize=(12,6), label='Used Price', color='blue')
    plt.plot(meansUsedDF['endTime'], fit_fn(x), linestyle='-', color='blue')
    plt.xticks(meansUsedDF.index, meansUsedDF['endTime'], rotation=90)
    ma = meansUsedDF['price'].rolling(5).mean()
    mstd = meansUsedDF['price'].rolling(5).std()
    plt.fill_between(mstd.index, ma-2*mstd, ma+2*mstd, color='k', alpha=0.2)
    plt.suptitle('Price Evolution of Used iPhone 6s 16GB')
    plt.savefig('Used Evolution.png')
    
    # Seller Refurbished
    plt.clf()
    refurbSellerDF, meansRefurbSellerDF, x, fit, fit_fn = regression(dataArrangedByCondition, 5, 'Seller refurbished')
    meansRefurbSellerDF.plot(x='endTime', y='price', figsize=(12,6), label='Seller Refurb Price', color='orange')       
    plt.plot(meansRefurbSellerDF['endTime'], fit_fn(x), linestyle='-', color='red')
    plt.xticks(meansRefurbSellerDF.index, meansRefurbSellerDF['endTime'], rotation=90)
    ma = meansRefurbSellerDF['price'].rolling(5).mean()
    mstd = meansRefurbSellerDF['price'].rolling(5).std()
    plt.fill_between(mstd.index, ma-2*mstd, ma+2*mstd, color='k', alpha=0.2)
    plt.suptitle('Price Evolution of Refurbished (Seller) iPhone 6s 16GB')
    plt.savefig('Refurb Seller Evolution.png')
       
    # Manufacturer Refurbished
    plt.clf()
    refurbManufDF, meansRefurbManuDF, x, fit, fit_fn = regression(dataArrangedByCondition, 5, 'Manufacturer refurbished')
    meansRefurbManuDF.plot(x='endTime', y='price', figsize=(12,6), label='Manufacturer Refurb Price', color='green')       
    plt.plot(meansRefurbManuDF['endTime'], fit_fn(x), linestyle='-', color='#637328')
    plt.xticks(meansRefurbManuDF.index, meansRefurbManuDF['endTime'], rotation=90)
    ma = meansRefurbManuDF['price'].rolling(5).mean()
    mstd = meansRefurbManuDF['price'].rolling(5).std()
    plt.fill_between(mstd.index, ma-2*mstd, ma+2*mstd, color='k', alpha=0.2)
    plt.suptitle('Price Evolution of Refurbished (Manufacturer) iPhone 6s 16GB')
    plt.savefig('Refurb Manufacturer.png')

    # Describe prices
    plt.clf()
    descDF = pd.DataFrame({'Used': usedDF['price'], 'Seller Refurb': refurbSellerDF['price'], 'Manuf Refurb': refurbManufDF['price']})
    desc = descDF.describe().transpose()
    plot = plt.subplot(frame_on=False)
    plot.xaxis.set_visible(False) 
    plot.yaxis.set_visible(False) 
    table = pd.plotting.table(plot, desc, loc='center')
    table.set_fontsize(12)
    table.scale(1,2)
    plt.savefig('Price Description.png')

    # Correlation Matrix of Used iPhone Dataframe
    plt.clf()
    corr = usedDF.corr()
    sb.heatmap(corr, cmap=sb.diverging_palette(250, 5), vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={'shrink': .5})
    plt.savefig('Correlation Matrix.png')

    pass