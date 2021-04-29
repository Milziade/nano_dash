import requests
import pandas as pd
import random
import colors


def get_json(nano_address):
    action = {
        'action': 'account_history',
        'account': nano_address,
        'count': '-1'
    }

    r = requests.post('https://mynano.ninja/api/node', json=action).json()
    if 'error' in r:
        return False
    return r['history']


def get_df(history):
    df = pd.DataFrame().from_dict(history)
    df = df.replace('nano_3kwppxjcggzs65fjh771ch6dbuic3xthsn5wsg6i5537jacw7m493ra8574x', 'FreeNanoFaucet.com')
    df = df.replace('nano_34prihdxwz3u4ps8qjnn14p7ujyewkoxkwyxm3u665it8rg5rdqw84qrypzk', 'nano-faucet.org')
    df = df.replace('nano_3pg8khw8gs94c1qeq9741n99ubrut8sj3n9kpntim1rm35h4wdzirofazmwt', 'nano.trade')
    df = df.replace('nano_1tyd79peyzk4bs5ok1enb633dqsrxou91k7y4zzo1oegw4s75bokmj1pey4s', 'Apollo Faucet')
    df['amount'] = [int(i)/10**30 for i in df['amount']]
    df['local_timestamp'] = pd.to_datetime(df['local_timestamp'], unit='s')
    del df['hash']
    del df['height']
    return df.to_dict('records'), df.columns.values


def get_balance(nano_address):
    action = {
        "action": "account_info",
        "account": nano_address
    }
    r = requests.post('https://mynano.ninja/api/node', json=action).json()
    return int(r['balance'])/10**30


def pie_chart(df):
    receive_acc = list(set(item['account'] for item in df if item['type'] == 'receive'))
    amount_receive = {i: 0 for i in receive_acc}
    send_acc = list(set(item['account'] for item in df if item['type'] == 'send'))
    amount_send = {i: 0 for i in send_acc}
    for d in df:
        key = d['account']
        if key in amount_receive:
            amount_receive[key] += d['amount']
        else:
            amount_send[key] += d['amount']

    return list(amount_receive.keys()), list(amount_receive.values()), \
           list(amount_send.keys()), list(amount_send.values())


def balance_over_time(df: dict):
    # Otteniamo il momento, il tipo di transazione e l'ammontare
    time = list([item['type'], item['amount'], str(item['local_timestamp']).split()[0]] for item in df)
    # Se l'account invia soldi, l'ammontare per il bilancio diviene negativo
    for item in time:
        if item[0] == 'send':
            item[1] = -item[1]
    time_n = [time[i][2] for i in range(len(time))]     # Date e orari di ogni transazione
    insta_bal = [time[i][1] for i in range(len(time))]
    overall_bal = [0]       # Bilancio cumulativo
    for i in range(len(time)):
        x = time[-1-i][1] + overall_bal[-1]
        overall_bal.append(x)
    overall_bal.pop(0)
    return overall_bal, list(reversed(time_n)), list(reversed(insta_bal))


def get_colors(n):
    # creates n different color
    colors_list = []
    for i in range(n):
        cols = colors.colors
        col = random.choice(cols)
        #cols.remove(col)
        colors_list.append(col)
    return colors_list
