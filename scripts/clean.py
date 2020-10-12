'''
Date: 2020-09-08
Author: Ali Eddeb

Purpose: Store functions used to clean scraped data.
'''

#IMPORT LIBRARIES
import numpy as np
import pandas as pd

#---------------------------------------------------------------------------------------

def convert_bools_to_int(dataframe):
    '''
    '''
    #convert boleans to int
    dataframe['avg_bid'] = np.where(dataframe['avg_bid'] == True, 1, 0)
    dataframe['verified_payment'] = np.where(dataframe['verified_payment'] == True, 1, 0)
    dataframe['contest'] = np.where(dataframe['contest'] == True, 1, 0)

    return dataframe


def clean_bids(dataframe):
    '''
    '''

    #FEATURE : bids
    #Remove words 'bids' and 'entries' and convert bids to int
    dataframe['bids'] = dataframe['bids'].str.replace('bids','').str.replace('entries','').str.strip().astype(int)

    return dataframe


def clean_daysr(dataframe):
    '''
    '''
    #FEATURE : days_remaining
    #Creating masks (True/False) for the 3 scenarios related to 'days_remiaining' feature

    #CASE 1: DAYS
    days_mask = dataframe['days_remaining'].str.contains('day')
    #CASE 2: HOURS
    hours_mask = dataframe['days_remaining'].str.contains('hour')
    #CASE 3: ENDED
    end_mask = dataframe['days_remaining'].str.contains('End')

    #Removing non-numeric part in days_remaining for all 3 cases
    
    #CASE 1: DAYS
    dataframe.loc[days_mask,'days_remaining'] = dataframe.loc[days_mask,'days_remaining'].str.replace(' days? left','',regex=True)
    #CASE 2: HOURS
    dataframe.loc[hours_mask,'days_remaining'] = dataframe.loc[hours_mask,'days_remaining'].str.replace(' hours? left','',regex=True).apply(lambda x : round(int(x)/24,3))
    #CASE 3: Job ENDED or ENDING
    dataframe.loc[end_mask,'days_remaining'] = dataframe.loc[end_mask,'days_remaining'].apply(lambda x : 0)

    #Finally, convert days_remaining to int
    dataframe['days_remaining'] = dataframe['days_remaining'].astype(int)

    return dataframe


def clean_price(dataframe):
    '''
    '''
    #FEATURE : price
    #remove 'hr'
    dataframe['price'] = dataframe['price'].str.replace(' / hr','')

    #Convert price range to min/max
    #creating price min and max columns
    dataframe['price_min'] = np.NaN
    dataframe['price_max'] = np.NaN

    #get index of prices that are ranges
    range_mask = dataframe['price'][dataframe['avg_bid'] == 0]

    #populate the min (first index) and max (last index) prices for price ranges
    dataframe.loc[range_mask.index, 'price_min'] = dataframe.loc[range_mask.index, 'price'].str.split().str[0]
    dataframe.loc[range_mask.index, 'price_max'] = dataframe.loc[range_mask.index, 'price'].str.split().str[-1]

    #Remove '$' sign for price, price_min and price_max
    for feature in ['price','price_min','price_max']:
        dataframe[feature] = dataframe[feature].str.replace('$','')

    #remove the price ranges and replace them with NaNs
    dataframe.loc[dataframe['avg_bid']==0,'price'] = np.NaN

    #edge case: convert 'min' to 0
    dataframe['price_min'] = dataframe['price_min'].str.replace('min','0')

    #Convert price, price_min and price_max to numeric (need to use float because of presence of NaNs)
    for feature in ['price','price_min','price_max']:
        dataframe[feature] = dataframe[feature].astype(float)

    return dataframe


def remove_duplicates(dataframe):
    '''
    '''

    return dataframe.drop_duplicates()


def clean_df(dataframe):
    '''
    '''

    return remove_duplicates(clean_price(clean_daysr(clean_bids(convert_bools_to_int(dataframe)))))