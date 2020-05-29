import fxcmpy
import numpy as np
from stocktrends import Renko
import statsmodels.api as sm
import time
import copy

class FXRenkoMACD:
    
    def __init__(self):
        self.pairs = ['EUR/USD','GBP/USD','USD/CHF','AUD/USD','USD/CAD','AUD/NZD','NZD/USD']

    def connectToFX_API(self):
        TOKEN = '########################################'
        con = fxcmpy.fxcmpy(access_token = TOKEN, log_level = 'error', server='demo')
        return con

    def MACD(self,DF,a,b,c):
        df = DF.copy()
        df["MA_Fast"]=df["Close"].ewm(span=a,min_periods=a).mean()
        df["MA_Slow"]=df["Close"].ewm(span=b,min_periods=b).mean()
        df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
        df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
        df.dropna(inplace=True)
        return (df["MACD"],df["Signal"])

        #method used for calculating renko charts
    def ATR(self,DF,n):
        df = DF.copy()
        df['H-L']=abs(df['High']-df['Low'])
        df['H-PC']=abs(df['High']-df['Close'].shift(1))
        df['L-PC']=abs(df['Low']-df['Close'].shift(1))
        df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
        df.iloc[0, df.columns.get_loc('TR')] =  df.iloc[0, df.columns.get_loc('H-L')]
        df['ATR'] = df['TR'].rolling(n).mean()
        #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
        df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
        return df2

    def slope(self,ser,n):
        slopes = [i*0 for i in range(n-1)]
        for i in range(n,len(ser)+1):
            y = ser[i-n:i]
            x = np.array(range(n))
            y_scaled = (y - y.min())/(y.max() - y.min())
            x_scaled = (x - x.min())/(x.max() - x.min())
            x_scaled = sm.add_constant(x_scaled)
            model = sm.OLS(y_scaled,x_scaled)
            results = model.fit()
            slopes.append(results.params[-1])
        slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
        return np.array(slope_angle)

    def renko_DF(self,DF):
        df = DF.copy()
        df.reset_index(inplace=True)
        df = df.iloc[:,[0,1,2,3,4,5]]
        df.columns = ["date","open","close","high","low","volume"]
        df2 = Renko(df)
        df2.brick_size = round(self.ATR(DF,120)["ATR"][-1],4)
        renko_df = df2.get_ohlc_data()
        renko_df["bar_num"] = np.where(renko_df["uptrend"]==True,1,np.where(renko_df["uptrend"]==False,-1,0))
        for i in range(1,len(renko_df["bar_num"])):
            if renko_df["bar_num"][i]>0 and renko_df["bar_num"][i-1]>0:
                renko_df["bar_num"][i]+=renko_df["bar_num"][i-1]
            elif renko_df["bar_num"][i]<0 and renko_df["bar_num"][i-1]<0:
                renko_df["bar_num"][i]+=renko_df["bar_num"][i-1]
        renko_df.drop_duplicates(subset="date",keep="last",inplace=True)

        return renko_df

    def renko_merge(self,fxDataframe):
        df = copy.deepcopy(fxDataframe)
        df["Date"] = df.index
        renko = self.renko_DF(df)
        renko.columns = ["Date","open","high","low","close","uptrend","bar_num"]
        merged_df = df.merge(renko.loc[:,["Date","bar_num"]],how="outer",on="Date")
        merged_df["bar_num"].fillna(method='ffill',inplace=True)
        merged_df["macd"]= self.MACD(merged_df,12,26,9)[0]
        merged_df["macd_sig"]= self.MACD(merged_df,12,26,9)[1]
        merged_df["macd_slope"] = self.slope(merged_df["macd"],5) #find slope of MACD with period of 5 days
        merged_df["macd_sig_slope"] = self.slope(merged_df["macd_sig"],5)  #find slope of MACD_sig with period of 5 days
        
        return merged_df

    
    def trade_signal(self,merged_df,long_short):
        signal = ""
        df = copy.deepcopy(merged_df)
        if long_short == "":
            if df["bar_num"].tolist()[-1]>=2 and df["macd"].tolist()[-1]>df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]>df["macd_sig_slope"].tolist()[-1]:
                signal = "Buy"
            elif df["bar_num"].tolist()[-1]<=-2 and df["macd"].tolist()[-1]<df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]<df["macd_sig_slope"].tolist()[-1]:
                signal = "Sell"
                print("inside sell Cmon")
                return signal
            else:
                signal ="No order"
                
        elif long_short == "long":
            if df["bar_num"].tolist()[-1]<=-2 and df["macd"].tolist()[-1]<df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]<df["macd_sig_slope"].tolist()[-1]:
                signal = "Close_Sell" #You close and then you initalize a sell since bear market is trending. Less than 2 renko etc
            elif df["macd"].tolist()[-1]<df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]<df["macd_sig_slope"].tolist()[-1]:
                signal = "Close" #You close the trade. Dont initiate new order
                
        elif long_short == "short":
            if df["bar_num"].tolist()[-1]>=2 and df["macd"].tolist()[-1]>df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]>df["macd_sig_slope"].tolist()[-1]:
                signal = "Close_Buy"
            elif df["macd"].tolist()[-1]>df["macd_sig"].tolist()[-1] and df["macd_slope"].tolist()[-1]>df["macd_sig_slope"].tolist()[-1]:
                signal = "Close"
        

        return signal
        

    def calculateOrderSignals(self, con):
        try:
            open_pos = con.get_open_positions()
            for currency in self.pairs:
                print(currency)
                long_short = ""
                if len(open_pos)>0:
                    open_pos_cur = open_pos[open_pos["currency"]==currency]
                    if len(open_pos_cur)>0:
                        if open_pos_cur["isBuy"].tolist()[0]==True:
                            long_short = "long"
                        elif open_pos_cur["isBuy"].tolist()[0]==False:
                            long_short = "short"   
                data = con.get_candles(currency, period='m5', number=250)
                fxDataframe = data.iloc[:,[0,1,2,3,8]]
                fxDataframe.columns = ["Open","Close","High","Low","Volume"]
              
                signal = self.trade_signal(self.renko_merge(fxDataframe),long_short)
                print("after signal")
                    
                self.createOrder(signal,currency, con)
        except:
            print("error encountered....skipping this iteration")



    def createOrder(self, signal, currency, con):
        pos_size = 10
        print("inside order")
        print(signal)
        signal = str(signal)
        currency = str(currency)
        
        if signal == "Buy":
            print("inside Buy create order")
            con.open_trade(symbol=currency, is_buy=True, is_in_pips=True, amount=pos_size, 
                                   time_in_force='GTC', stop=-8, trailing_step =True, order_type='AtMarket')
            print("New long position initiated for ", currency)
        
        elif signal == "Sell":
            print("inside Sell create order")
            con.open_trade(symbol=currency, is_buy=False, is_in_pips=True, amount=pos_size, 
                                   time_in_force='GTC', stop=-8, trailing_step =True, order_type='AtMarket')
            print("New short position initiated for ", currency)
        elif signal == "Close":
            con.close_all_for_symbol(currency)
            print("All positions closed for ", currency)
        elif signal == "Close_Buy":
            con.close_all_for_symbol(currency)
            print("Existing Short position closed for ", currency)
            con.open_trade(symbol=currency, is_buy=True, is_in_pips=True, amount=pos_size, 
                                   time_in_force='GTC', stop=-8, trailing_step =True, order_type='AtMarket')
            print("New long position initiated for ", currency)
        elif signal == "Close_Sell":
            con.close_all_for_symbol(currency)
            print("Existing long position closed for ", currency)
            con.open_trade(symbol=currency, is_buy=False, is_in_pips=True, amount=pos_size, 
                                   time_in_force='GTC', stop=-8, trailing_step =True, order_type='AtMarket')
            print("New short position initiated for ", currency)
        else:
            print(signal)


    def timer(self):      
        starttime=time.time()
        timeout = time.time() + 60*60*1 # run script for 1 hour
        con = self.connectToFX_API() #get API connection  
        while time.time() <= timeout:
            try:
                print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                self.calculateOrderSignals(con) #calculate signals
                time.sleep(300 - ((time.time() - starttime) % 300.0)) # 5 minute interval between each new execution
            except KeyboardInterrupt:
                print('\n\nKeyboard exception received. Exiting.')
                exit()

        # Close all positions and exit trades
        for currency in self.pairs:
            print("closing all positions for ",currency)
            con.close_all_for_symbol(currency)
        print("closing connection with FXCM")
        con.close()

def main():
    obj = FXRenkoMACD()
    obj.timer()

main()



