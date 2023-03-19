import tkinter as tk
import time

from bitcoinlib.wallets import wallet_create_or_open
from bitcoinlib.mnemonic import Mnemonic

def generate_mnemonic():
    mnemonic = Mnemonic().generate(strength=256)
    return mnemonic

def create_wallet(mnemonic):
    wallet_name = f"my_wallet_{int(time.time())}"  # Generate a unique wallet name using the current timestamp
    wallet = wallet_create_or_open(wallet_name, keys=mnemonic, network='bitcoin', witness_type='segwit')
    return wallet.get_key().address

def on_generate_click():
    mnemonic = generate_mnemonic()
    address = create_wallet(mnemonic)
    mnemonic_label.config(text=mnemonic)
    address_label.config(text=address)

def main():
    global mnemonic_label
    global address_label

    root = tk.Tk()
    root.title("BTC Wallet Generator")

    title_label = tk.Label(root, text="Bitcoin Wallet Generator", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    mnemonic_title = tk.Label(root, text="Mnemonic Seed:", font=("Helvetica", 12))
    mnemonic_title.pack(pady=5)

    mnemonic_label = tk.Label(root, text="", font=("Helvetica", 10))
    mnemonic_label.pack(pady=5)

    address_title = tk.Label(root, text="Wallet Address:", font=("Helvetica", 12))
    address_title.pack(pady=5)

    address_label = tk.Label(root, text="", font=("Helvetica", 10))
    address_label.pack(pady=5)

    generate_button = tk.Button(root, text="Generate Wallet", command=on_generate_click)
    generate_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
