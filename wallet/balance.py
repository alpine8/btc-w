from bitcoinlib.keys import HDKey
from bitcoinlib.services.services import Service

def import_wallet_from_mnemonic(mnemonic):
    bip84_derivation_path = "m/84'/0'/0'/0/0"
    master_key = HDKey.from_passphrase(mnemonic, network='bitcoin', witness_type='segwit')
    key = master_key.subkey_for_path(bip84_derivation_path)
    address = key.address()
    print("Imported wallet address:", address)
    return key



def display_balance(key):
    service = Service(network='bitcoin')
    balance = service.getbalance(key.address())
    print(f"Wallet balance: {balance} satoshis")

def main():
    mnemonic = input("Enter your mnemonic seed phrase: ")
    imported_key = import_wallet_from_mnemonic(mnemonic)
    display_balance(imported_key)

if __name__ == '__main__':
    main()
