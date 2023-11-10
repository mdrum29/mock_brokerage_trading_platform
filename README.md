# mock_brokerage_trading_platform
This code replicates a basic brokerage trading platform.
The user can BUY and SELL any exchange listed stock. The app keeps track of and graphs portfolio balances over time, displays recent transactions updated in real-time and provides real-time quotes to user.
The platform connects to Alpaca.Markets Paper-Trading API. Therefore, all of these trades are not real but the data is accurate and in real-time. In addition, a user could create a real account on Alpaca and plug this into the live trading API.


Part 1:
This screenshot is what you will see when you load up the server.
1. The real-time cash available to trade is display towards the right in the order section.
2. The historical weekly balance is displayed in the middle with a real time portfolio balances that refreshes every 5 seconds while the market is open.
3. In the bottom right, there is a real-time pie chart showing the users current asset allocation.

   
![image](https://github.com/mdrum29/mock_brokerage_trading_platform/assets/96875916/0e25d2d4-ed22-438b-93d6-89918440c860)




Part 2:
1. On the left, order details can be submitted. When a user enters a ticker, a real-time quote will be displayed for that stock above the submit button.
2. Once submit is clicked, the app will submit the order to the Alpaca API.

   
![trade1](https://github.com/mdrum29/mock_brokerage_trading_platform/assets/96875916/0a2d9218-ea50-4036-9de2-f6ed4f449fd5)



Part 3:
1. Once submitted, the user will recieve a confirmation message just below the submit button to confirm order was successful or failed.
2. Then once the trade is filled, it will appear in the transaction history below.
3. Finally, the new postion will be displayed in the pie chart in the bottom right and the cash available in the order window will be updated.

   
![start](https://github.com/mdrum29/mock_brokerage_trading_platform/assets/96875916/c2281899-4d8c-4d4b-a7f3-ed58fb6f993e)
