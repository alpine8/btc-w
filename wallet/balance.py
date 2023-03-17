from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.keys import HDKey

def import_wallet_from_mnemonic(mnemonic):
    key = HDKey.from_passphrase(mnemonic)
    wallet = wallet_create_or_open("imported_wallet", keys=key, network='bitcoin', witness_type='segwit')
    print("Imported wallet address:", wallet.get_key().address)
    return wallet

def display_balance(wallet):
    wallet.utxos_update()
    balance = wallet.balance
    print(f"Wallet balance: {balance} satoshis")

def main():
    mnemonic = input("Enter your mnemonic seed phrase: ")
    imported_wallet = import_wallet_from_mnemonic(mnemonic)
    display_balance(imported_wallet)

if __name__ == '__main__':
    main()
