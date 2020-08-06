## Blockchain with Python Homework - Steffen Westerburger ##
## Multi-Blockchain Wallet in Python ##

**What does the HD wallet do?**

According to Investopedia the HD wallet is a hierarchical deterministic wallet, which enables the used to automatically generate a hierarchical tree-like structure of private and public addresses (keys). This makes the process very easy, and solves the problem of users having the manually generate keys on their own. 

**How is the wallet built?**

*needed dependencies*

* PHP
* hd-wallet-derive tool  (see readme of this tool)
* bit library in Python
* web3.py Python Ethereum library

To build the wallet we use the command line tool together with `hd-wallet-derive`. There is no direct tool in Python yet, so we need to integrate this script in the backend of our Python. 

After installing the tools/dependencies, you can make a connection with the HD wallet derive in python, using the following command. This will derive the wallet:

`def derive_wallets (mnemonic, coin, num):`
    
    `command = f'./derive -g --mnemonic="{mnemonic}" --coin="{coin}" --numderive="{num}" --cols=index,path,address,privkey,pubkey,pubkeyhash,xprv,xpub --format=json'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    
    keys = json.loads(output)
    
    return keys

**A BTC Testnet Transaction**

![BTC Python Transaction](screenshots/btc_tx_python.png)

![BTC Web Confirmation](screenshots/btc_tx_web.png)

**A Ethereum Transaction**

![ETH Python Transaction](screenshots/eth_tx_python.png)

![ETH Ganache Transaction](screenshots/eth_tx_ganache.png)

![ETH Ganache Transaction](screenshots/eth_tx_ganache2.png)
