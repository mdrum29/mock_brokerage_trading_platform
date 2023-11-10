import requests
from api_keys import api_secret,api_key
import pandas as pd

endpoint = "https://paper-api.alpaca.markets"

headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "APCA-API-KEY-ID": api_key, 
        "APCA-API-SECRET-KEY":api_secret,
        }


def order(isBuySide, qty, ticker):
    """
    Args:
        isBuySide -> bool
        qty -> int
        ticker -> str
    """
    
    if isBuySide == True:
        side = "buy"
    elif isBuySide == False:
        side = "sell"
    
    payload = {
        "side": side,
        "type": "market",
        "time_in_force": "day",
        "qty": str(qty),
        # "notional": "1000", # dollar amount
        "symbol": ticker,
        }
    
    orders_ep = "/v2/orders"
    orders = requests.post(endpoint+orders_ep,headers=headers, json=payload).json()
    print("order submittted.")

    orders['id']

    order_details = requests.get(endpoint+orders_ep+'/'+orders['id'],headers=headers, json=payload).json()

    confirmation = {"B/S": order_details['side'],"ticker": order_details['symbol'], "quantity": order_details['qty']}

    return confirmation

def getHoldings():
    pos_ep = '/v2/positions'
    positions = requests.get(endpoint+pos_ep,headers= headers).json()

    total_asset_value = 0
    holdings = []
    for _, a in enumerate(positions):
        asset = a['symbol']
        value = float(a['qty']) * float(a['avg_entry_price'])
        holdings.append((asset, value))

        total_asset_value += value
    holdings_df = pd.DataFrame(holdings, columns=['Ticker', "Value"])
    return holdings_df, total_asset_value

def getHistoricalBalances():
    pf_history_ep = '/v2/account/portfolio/history'
    pf_history = requests.get(endpoint+pf_history_ep,headers= headers).json()
    
    time_frame = pf_history['timestamp']
    balance = pf_history['equity']
    
    date_range = []
    balances = []
    for idx, t in enumerate(time_frame):
        date = pd.to_timedelta(t, unit='s') + pd.to_datetime('1960-1-1')
        date = date.strftime('%b %d')
        date_range.append(date)

        balances.append( 500000 if balance[idx] == 0 else balance[idx])
        bals_df = pd.DataFrame({'date': date_range, 'balance': balances,})

    return bals_df

def getTransactionHistory():
    cols = ['Type', 'Ticker', 'Notional', 'Qty', 'Avg Price','Status','Submitted At',]
    transaction_history_df = pd.DataFrame()
    
    tranx_ep = "/v2/orders?status=all&limit=10"
    tranx_history = requests.get(endpoint+tranx_ep,headers= headers).json()
    for idx, t in enumerate(tranx_history):
        submitted = pd.to_datetime(t['submitted_at']).strftime('%b %d %H:%M')
        ticker = t['symbol']
        qty = round(float(t['filled_qty'] if t['qty'] == None else t['qty']),4)
        avg_price = round(float(t['filled_avg_price']),4)
        notional = round(float(qty) * float(avg_price),4)
        side = t['side'].upper()
        status = t['status'].upper()
        df = pd.DataFrame([side, ticker, notional, qty, avg_price, status, submitted],)

        transaction_history_df = pd.concat([transaction_history_df, df.T])

    transaction_history_df.columns = cols
    th_df = transaction_history_df.reset_index(drop=True)

    return th_df

def get_cash():
    acct_ep = '/v2/account'
    getAcct = requests.get(endpoint+acct_ep,headers= headers).json()

    cash_balance = float(getAcct['cash'])
    return cash_balance

def get_live_price(ticker,side):
    url = f"https://data.alpaca.markets/v2/stocks/{ticker}/quotes/latest?feed=iex"
    lp = requests.get(url,headers= headers).json()
    if 'message' in lp:
        return "Ticker Invalid "
    else:
        if side == 'BUY':
            live_price = lp['quote']['ap']
        elif side == 'SELL':
            live_price = lp['quote']['bp']
        return live_price

if __name__ == "__main__":
    # confirmation = order(False, 50, "AAPL")
    # holdings, total_asset_value = getHoldings()
    # th_df = getTransactionHistory()
    # dr, bls = getHistoricalBalances()
    # lp = get_live_price('TSLA', 'BUY')
    C = get_cash()
    print("")