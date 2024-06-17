This Package is intended for use with Python.

To use this package: 
##1. Install the dependancies:
slenium:
```
pip install selenium
```
If you don't already have dotenv installed you'll need to do this also.
dotenv:
```
pip install dotenv
```

for older versions of python see the user.py file for all dependancies.

##2. Create the .env file from the .env.template and update the BEARER_TOKEN with your Twitter API's App bearer token. Please note this script requires a Basic suscription or better.

Rename .env.template to .env and replace your_bearer_token with your actual App's bearer token

##3. Replace the handles in the FOLLOW_USERS array

You can add multiple twitter handles to this script, however the more you add the longer the delay time between updates for each user since it iterates over this list. It's recommended to instead use one user handle per script and run multiple instances of the script, changing handle between instances. 

##Future Improvements:
We can address the iteration issue by opening threads in the get_tweet_count function. 
Would like to do a contract verification to ensure the address is a valid token address.
Would like to add optional GPT verification to aviod potential influencer traps 
Would like to include optional filters including token age, liquidity pool age.
Build a swapping bot which can take token or lp addresses and perform a swap. *
Would like to do optional test transactions to avoid honeypots before making the automated swap. *

* To build a swap bot we need to: 
1. Have a script that creates, saves and loads private keys for use when swapping should display address on load so you know which address to fund. 
2. Takes a token contract address, asset to swap (SOL usually) and an amount. May be a good idea to allow amount to be max/wallet.balance by polling the balance at the beginning of the script and every time a swap completes.
3. Checks Raydium for the LP and obtains the address, age and any other relevant data depending on which options were selected.
4. Performs any optional checks such as max age, liquidity locks, honeypot checks, etc.
5. Makes swap.
6. Transfers tokens to another address, saving just enough from the swap for gas.

Would like to build swap bot to work with multiple platforms including pump.fun and check multiple LPs beyond just Raydium.

To support the development of this open source twitter bot send donations to ABHB2A2Em14GBXY6AxKprXHJifr7KPjUKq983dFsdhJ7 so I can pay developers in our community to continue working on it.
