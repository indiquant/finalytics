'''
Created on Sep 17, 2016

@author: ashokmuthusamy

Adopted from http://www.codeandfinance.com/finding-implied-vol.html
'''

import pandas as pd
import numpy as np
import os
from  scipy.stats import norm
import datetime as dt

def find_vol(target_value, call_put, S, K, T, r):
    MAX_ITERATIONS = 100
    PRECISION = 1.0e-5

    sigma = 2
    for i in np.arange(0, MAX_ITERATIONS):
        price = bs_price(call_put, S, K, T, r, sigma)
        vega = bs_vega(call_put, S, K, T, r, sigma)

        price = price
        diff = target_value - price  # our root

        print(i, sigma, diff)

        if (abs(diff) < PRECISION):
            return sigma
        sigma = sigma + diff/vega # f(x) / f'(x)

        if sigma<=0:
            sigma = 0.5
    # value wasn't found, return best guess so far
    return sigma


n = norm.pdf
N = norm.cdf

def bs_price(cp_flag,S,K,T,r,v,q=0.0):
    d1 = (np.log(S/K)+(r+v*v/2.0)*T)/(v*np.sqrt(T))
    d2 = d1-v* np.sqrt(T)
    if cp_flag == 'c':
        price = S* np.exp(-q*T)*N(d1)-K*np.exp(-r*T)*N(d2)
    else:
        price = K*np.exp(-r*T)*N(-d2)-S*np.exp(-q*T)*N(-d1)
    return price

def bs_vega(cp_flag,S,K,T,r,v,q=0.0):
    d1 = (np.log(S/K)+(r+v*v/2.0)*T)/(v*np.sqrt(T))
    return S * np.sqrt(T)*n(d1)

if __name__ == '__main__':
    
    input_file_path = '/Users/ashokmuthusamy/Documents/indiaquant/options_intraday.txt'
    
    input_df = pd.read_table(os.path.expandvars(input_file_path), )
    input_df = input_df.head()
    #print(input_df.head())
    
    input_df['expiry']  = pd.to_datetime( input_df['expiry'], format='%Y%m%d' )
    input_df['recdate']  = pd.to_datetime( input_df['recdate'] , format='%Y%m%d' )
    
    input_df['time_to_expiry'] = (input_df['expiry'] - input_df['recdate']) /  np.timedelta64(1, 'D') / 365.0
    input_df['opt_type'] = input_df['opt_type'].str.lower()
    print(input_df.head())
    #print(input_df.info() )
    
    
    r = 0.02
    
    for _,row in input_df.head(10).iterrows():
        #print (row)
        '''
        print (np.nanmean([ row['bidpx'], row['askpx'] ], axis=0),
                   row['opt_type'], row['spot'], row['strike'], 
                row['time_to_expiry'], r)
        '''
        if pd.isnull(np.nanmean([ row['bidpx'], row['askpx'] ],axis=0) ):
            continue

        vol = find_vol( np.nanmean([ row['bidpx'], row['askpx'] ], axis=0),
                   row['opt_type'], row['spot'], row['strike'], 
                row['time_to_expiry'], r)
        print (vol * 100)
        
    
    
    '''
    V_market = 17.5
    K = 585
    T = (dt.date(2014,10,18) - dt.date(2014,9,8)).days / 365.
    S = 586.08
    r = 0.0002
    cp = 'c' # call option
    
    implied_vol = find_vol(V_market, cp, S, K, T, r)
    
    print( 'Implied vol: %.2f%%' % (implied_vol * 100) )
    
    print ('Market price = %.2f' % V_market )
    print ('Model price = %.2f' % bs_price(cp, S, K, T, r, implied_vol) )
    '''