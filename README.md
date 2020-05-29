# Automated-ForexTradingAlgorithms
Repository contains Forex Algorithms using automated strategies with FXCM, Oanda REST APIs.

# [FX_RenkoMACD.py Algorithm Description](https://github.com/juanfp900/Automated-ForexTradingAlgorithms/blob/master/FXCMForexBot/FX_RenkoMACD.py)
## Algorithm Description
This algorithim uses the FXCM broker API to trade currency pairs. Decisions for placing orders depends 
on MACD, Renko Chart indicators. The algorithm is intended to work for both 1min and 5min candles.

To **buy orders (long position)** the following conditions will need to be met:
  1. The MACD (12,26) will need to trend higher the signal MACD line (9)
    - MACD >= Signal-MACD
  2. The slope of MACD should be higher than the signal MACD line slope. 
    - MACD slope > Signal-MACD slope
  3. There should be two consecutive green Renko Bars trending up.
 
 
 To **sell orders (short position)** the following conditions will need to be met:
  1. The MACD (12,26) will need to trend below the signal MACD line (9)
    - MACD =< Signal-MACD
  2. The slope of MACD should be less than the signal MACD line slope.
    - MACD slope < Signal-MACD slope
  3. There should be two consecutive green Renko Bars trending up.
    
 
 **If neither** condition is met. A no order is printed to console for that specific currency pair and the algorithm loops to next curency pair

# The Algorithm can be ran locally or using Amazon Web Service EC2 instance
To run on AWS you must create AWS account and navigate to the AWS EC2 portal:
       1.Navigate to EC2 dashboard
       2.Select Create New Instance.
       3. Select Amazon Linux 2 AMI (HVM), SSD Volume Type (Free tier)
       4. Select General Purpose t2.micro (Free tier)
       5. Once EC22 instance is created you  must save the .pem key file you get in a local directory. 
       6. You will need to SSH using this key to connect to an Amazon EC2 instance 
       7. The EC2 instance will not have Python, Pip or any packages installed. 
          - You will need to install Python3.7, Pip in the Amazon EC2 instance  
       8. Note: Best to send your requirements.txt file to EC2 instead of installing individual packages using Pip in AWS.
       
       
       
       
       






