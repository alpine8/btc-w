from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.mnemonic import Mnemonic

def generate_mnemonic():
    mnemonic = Mnemonic().generate()
    print("Mnemonic seed:", mnemonic)
    return mnemonic

def create_wallet(mnemonic):
    wallet = wallet_create_or_open("my_wallet", keys=mnemonic, network='bitcoin', witness_type='segwit')
    print("Wallet created with address:", wallet.get_key().address)  # Updated this line
    return wallet

def display_balance(wallet):
    wallet.utxos_update()  # Update the wallet unspent transaction outputs
    balance = wallet.balance  # Access the wallet balance
    print(f"Wallet balance: {balance} satoshis")


def main():
    mnemonic = generate_mnemonic()
    wallet = create_wallet(mnemonic)
    display_balance(wallet)

if __name__ == '__main__':
    main()
