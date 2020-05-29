# Automated-ForexTradingAlgorithms
Repository contains Forex Algorithms using automated strategies with FXCM, Oanda REST APIs.

### The following algorithms will use the following broker to trade currencies.
### Trades will be displayed in the open position section shown in the below screenshot in real time.
![Image of FXCM broker](https://github.com/juanfp900/Automated-ForexTradingAlgorithms/blob/master/FXCMForexBot/Images/FXCM.png)

# [FX_RenkoMACD.py](https://github.com/juanfp900/Automated-ForexTradingAlgorithms/blob/master/FXCMForexBot/FX_RenkoMACD.py)
## FX_RenkoMACD Algorithm Description
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

# Run Algorithm on Amazon Web Service EC2 instance
To run on AWS you must create a free **[AWS account](https://aws.amazon.com/free/) and navigate to the AWS EC2 portal:
1. Navigate to EC2 dashboard.
2. Select Create New Instance.
3. Select Amazon Linux 2 AMI (HVM), SSD Volume Type (Free tier).
4. Select General Purpose t2.micro (Free tier).
5. Once EC2 instance is created you  must save the .pem key file you get in a local directory. 
6. You will need to SSH using this key to connect to your Amazon account. 
7. The EC2 instance will not have Python, Pip or any packages installed. 
    - You will need to install Python3.7, Pip in the Amazon EC2 instance using: **[AWS Elastic Beanstalk Tutorial](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html)
8. Note: It is best to send the requirements.txt file containing all Python packages to EC2 rather than installing each individual package using Pip. 
10. Run the Python script on AWS EC2. 
9. After running program you should **Terminate** your EC2 instance to prevent hidden charges. Refer to below images 

![Image of Terminate Button](https://github.com/juanfp900/Automated-ForexTradingAlgorithms/blob/master/FXCMForexBot/Images/AWS_terminateMenu.png)

![Image of FXCM](https://github.com/juanfp900/Automated-ForexTradingAlgorithms/blob/master/FXCMForexBot/Images/AWS_terminateMenu.png)




       
       
       
       
       






