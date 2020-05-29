# Automated-ForexTradingAlgorithms
Repository contains Forex Algorithms using automated strategies with FXCM, Oanda REST APIs

#Algorithm Description
 FXCMForexBot(https://github.com/juanfp900/Automated-ForexTradingAlgorithms/blob/master/FXCMForexBot/FX_RenkoMACD.py)

# Algorithm Description
This algorithim uses the FXCM broker API to trade currency pairs. Decisions for placing orders depends 
on MACD, Renko Chart indicators. The algorithm is intended to work for both 1min and 5min candles.
To buy orders (long position) the following conditions will need to be met:
  1. The MACD (12,26) will need to trend higher the signal MACD line (9)
    - MACD > Signal-MACD
  2. The slope of MACD should be higher than the signal MACD line slope
  3. There should be two consecutive green Renko Bars


# The Algorithm can be ran locally or using Amazon Web Service EC2 instance. (AWS)

To run on AWS you must create AWS account and navigate to the AWS EC2 portal.
Select 




