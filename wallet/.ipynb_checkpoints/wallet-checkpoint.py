# imports
from constants import *
import os
from dotenv import load_dotenv
import json
import subprocess
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from bit import wif_to_key, PrivateKeyTestnet
from bit.network import NetworkAPI
from eth_account import Account

# load ev
load_dotenv()

# load w3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer =0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# mnemonic key
mnemonic = os.getenv('MNEMONIC')

# derive wallet function

def derive_wallets (mnemonic, coin, num):
    
    command = f'./derive -g --mnemonic="{mnemonic}" --coin="{coin}" --numderive="{num}" --cols=index,path,address,privkey,pubkey,pubkeyhash,xprv,xpub --format=json'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    
    keys = json.loads(output)
    
    return keys

derive_wallets(mnemonic, BTC, 3)

# create object called coins that derives ETH and BTCTEST

coins = {'eth':derive_wallets(mnemonic,ETH, 3),'btc-test': derive_wallets(mnemonic,BTCTEST,3)}
coins

# eth_pk = coins['eth'][1]['privkey']
# btc_pk = coins['btc-test'][1]['privkey']

# create three more functions

def priv_key_to_account (coin, priv_key):

    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

# keys to first sister account 
# eth_key = priv_key_to_account(ETH, eth_pk)
# btc_key = priv_key_to_account(BTCTEST, btc_pk)

#

def create_tx (coin, account, recipient, amount):
    
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "to": recipient,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        } 
    
    if coin == BTCTEST:
        
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)]) 
    

# test by sending to 3rd sister account 

# eth_account = coins['eth'][2]['address']
# btc_account = coins['btc-test'][2]['address']

# trx = create_tx(ETH, eth_key, eth_account , 1)
# trx
    
#    

def send_tx(coin,account, recipient, amount):
    
    tx = create_tx(coin,account,recipient,amount)
    signed_tx = account.sign_transaction(tx)
    
    if coin == ETH:
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result.hex()
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)
    

## send BTC transaction (using funded accounts) ##

# using different mnemonic code which I used prior to fund BTC Testnet account - since this is for testing purposes it doesnt matter to show the mnemonic

mnemonic2 = 'frown bunker illness hospital sibling tenant capable someone act royal lazy plunge'

# Derive the wallet and create keys
btc_wallet = derive_wallets(mnemonic2, BTCTEST, 3)
btc_pk = btc_wallet[0]['privkey']
btc_key = priv_key_to_account(BTCTEST, btc_pk)

# Create transaction
btc_trx = create_tx(BTCTEST, btc_key, 'mrCkt1p8bVGygXtnK3H2ViH2ghQqs3Crse', 0.000001)
btc_trx

# Send transaction
send_tx(BTCTEST, btc_key, 'mrCkt1p8bVGygXtnK3H2ViH2ghQqs3Crse', 0.000001)


## Send Ethereum using Ganache blockchain based on mnemonic that was generated in this exercise ## 

# Derive the wallet and create keys

eth_wallet = derive_wallets(mnemonic, ETH, 3)
eth_pk = eth_wallet[0]['privkey']
eth_key = priv_key_to_account(ETH, eth_pk)

# Create transaction
eth_trx = create_tx(ETH, eth_key, '0xc467e0EBC46353412374d002DC3Ede9D013a5ca9', 20)
eth_trx

# Send transaction
send_tx(ETH, eth_key, '0xc467e0EBC46353412374d002DC3Ede9D013a5ca9', 20)