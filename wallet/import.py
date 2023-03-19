import hashlib
from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.keys import HDKey

def import_wallet_from_mnemonic(mnemonic):
    key = HDKey.from_passphrase(mnemonic)
    wallet_id = "imported_wallet_" + hashlib.sha256(mnemonic.encode()).hexdigest()
    wallet = wallet_create_or_open(wallet_id, keys=key, network='bitcoin', witness_type='segwit')
    print("Imported wallet address:", wallet.get_key().address)
    return wallet

def main():
    mnemonic = input("Enter your mnemonic seed phrase: ")
    imported_wallet = import_wallet_from_mnemonic(mnemonic)
    # You can add more wallet-related functions here

if __name__ == '__main__':
    main()
