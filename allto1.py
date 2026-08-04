from web3 import Web3

# Konfigurasi jaringan blockchain opBNB
RPC_URL = "https://opbnb-mainnet-rpc.bnbchain.org/"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Membaca private keys dari file txt
with open("accounts.txt", "r") as file:
    PRIVATE_KEYS = [line.strip() for line in file.readlines() if line.strip()]

DESTINATION_ADDRESS = "0x4b05CAD2a8E10DFdE15D0ec4239bCB94e107ccbC"

# Jumlah sisa saldo yang ingin disisipkan di wallet (0.0000005 BNB dalam Wei)
RESERVE_AMOUNT = Web3.to_wei(0.0000005, 'ether')

# Mendapatkan Chain ID opBNB
CHAIN_ID = web3.eth.chain_id

def send_transaction(private_key):
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)

    # Cek saldo akun
    balance = web3.eth.get_balance(account.address)
    
    # Hitung perkiraan biaya gas (transfer standar BNB = 21000 gas)
    gas_limit = 21000
    gas_price = web3.eth.gas_price
    gas_fee = gas_limit * gas_price  

    # Hitung jumlah maksimum yang bisa dikirim (Saldo - Biaya Gas - Saldo Cadangan)
    amount_to_send = balance - gas_fee - RESERVE_AMOUNT

    # Jika saldo tidak cukup untuk membayar gas fee + cadangan
    if amount_to_send <= 0:
        print(f"Skipping {account.address}: Insufficient funds (Balance: {web3.from_wei(balance, 'ether')} BNB)")
        return None  # Lewati transaksi ini

    transaction = {
        'to': DESTINATION_ADDRESS,
        'value': amount_to_send,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': CHAIN_ID
    }

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return web3.to_hex(tx_hash)

if __name__ == "__main__":
    print(f"Connected to opBNB | Using Chain ID: {CHAIN_ID}")

    for key in PRIVATE_KEYS:
        try:
            tx_hash = send_transaction(key)
            if tx_hash:
                print(f"Transaction sent successfully: {tx_hash}")
            else:
                print("Skipped due to insufficient funds.")
        except Exception as e:
            print(f"Error processing account: {e}")

    print("Semua Aset Sudah terkirim.")
