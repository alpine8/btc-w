import tkinter as tk
from tkinter import ttk
import bitcoinlib
import requests
import qrcode
from PIL import ImageTk, Image
from ttkthemes import ThemedTk
from bit import Key, PrivateKeyTestnet
from bitcoinlib.wallets import Wallet
from bitcoinlib.encoding import addr_bech32_to_pubkeyhash


class BitcoinWalletGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bitcoin Wallet Generator")

        # Create frames for different sections
        self.new_wallet_frame = ttk.LabelFrame(self.master, text="New Wallet")
        self.import_wallet_frame = ttk.LabelFrame(self.master, text="Import Wallet")
        self.balance_frame = ttk.LabelFrame(self.master, text="Balance")
        self.transactions_frame = ttk.LabelFrame(self.master, text="Transactions")

        # Add widgets to the new wallet frame
        self.generate_button = ttk.Button(self.new_wallet_frame, text="Generate Wallet", command=self.generate_wallet)
        self.seed_phrase_label = ttk.Label(self.new_wallet_frame, text="Seed Phrase: ")
        self.seed_phrase_entry = ttk.Entry(self.new_wallet_frame, width=50)
        self.address_label = ttk.Label(self.new_wallet_frame, text="Address: ")
        self.address_entry = ttk.Entry(self.new_wallet_frame, width=50)
        self.qr_code_label = ttk.Label(self.new_wallet_frame)

        # Add widgets to the import wallet frame
        self.import_button = ttk.Button(self.import_wallet_frame, text="Import Wallet", command=self.import_wallet)
        self.seed_phrase_import_label = ttk.Label(self.import_wallet_frame, text="Seed Phrase: ")
        self.seed_phrase_import_entry = ttk.Entry(self.import_wallet_frame, width=50)
        self.public_key_import_label = ttk.Label(self.import_wallet_frame, text="Public Key: ")
        self.public_key_import_entry = ttk.Entry(self.import_wallet_frame, width=50)

        # Add widgets to the balance frame
        self.balance_button = ttk.Button(self.balance_frame, text="Check Balance", command=self.check_balance)
        self.balance_label = ttk.Label(self.balance_frame, text="Current Balance: ")
        self.balance_value = ttk.Label(self.balance_frame, text="")

        # Add widgets to the transactions frame
        self.transactions_button = ttk.Button(self.transactions_frame, text="Check Transactions", command=self.check_transactions)
        self.transactions_label = ttk.Label(self.transactions_frame, text="Last 3 Transactions: ")
        self.transactions_value = ttk.Label(self.transactions_frame, text="")

        # Pack the widgets into the frames
        self.new_wallet_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.generate_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.seed_phrase_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.seed_phrase_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.address_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.address_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.qr_code_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.import_wallet_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.import_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.seed_phrase_import_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.seed_phrase_import_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.public_key_import_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.public_key_import_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.balance_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.balance_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.balance_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.balance_value.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.transactions_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.transactions_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.transactions_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.transactions_value.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def generate_wallet(self):
        # Generate a new bitcoin wallet using the bitcoinlib library
        mnemonic = bitcoinlib.mnemonic.Mnemonic()
        seed_phrase = mnemonic.generate()

        # Generate a new bitcoin wallet using the seed phrase
        wallet = bitcoinlib.keys.HDKey.from_seed(mnemonic.to_seed(seed_phrase))

        # Derive the bech32 (BC1) address from the wallet
        key = wallet.subkey_for_path("84'/0'/0'/0/0")
        pubkeyhash = key.hash160
        address = bitcoinlib.encoding.pubkeyhash_to_addr_bech32(pubkeyhash, prefix='bc')

        # Update the seed phrase and address entries with the generated values
        self.seed_phrase_entry.delete(0, tk.END)
        self.seed_phrase_entry.insert(0, seed_phrase)
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, address)

        # Generate and display the QR code
        self.show_qr_code(address, self.qr_code_label)

    def check_balance(self):
        # Get the address value from the input field
        address = self.address_entry.get()

        # Check the balance for a bitcoin address using the blockchain.com API
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = requests.get(url)

        if response.status_code == 200:
            # Show the balance in satoshis
            balance = int(response.text)
            self.balance_value.config(text=str(balance) + " satoshis")

            # Generate the QR code for the address
            self.show_qr_code(address, self.qr_code_label_balance)
        else:
            self.balance_value.config(text="Error checking balance")

    def import_wallet(self):
        # Get the seed phrase and public key values from the input fields
        seed_phrase = self.seed_phrase_import_entry.get()
        public_key = self.public_key_import_entry.get()

        if seed_phrase:
            # Generate a seed using the seed phrase
            mnemonic = bitcoinlib.mnemonic.Mnemonic()
            seed = mnemonic.to_seed(seed_phrase)

            # Import a bitcoin wallet using the seed
            wallet = bitcoinlib.keys.HDKey.from_seed(seed)

            # Derive the bech32 (BC1) address using the path m/84'/0'/0'/0/0 (default for the first Bitcoin address)
            derived_key = wallet.subkey_for_path("84'/0'/0'/0/0")
            pubkeyhash = derived_key.hash160
            address = bitcoinlib.encoding.pubkeyhash_to_addr_bech32(pubkeyhash, prefix='bc')

        elif public_key:
            # Import a bitcoin wallet using the public key
            derived_key = bitcoinlib.keys.HDKey.from_public_key_hex(public_key)
            pubkeyhash = derived_key.hash160
            address = bitcoinlib.encoding.pubkeyhash_to_addr_bech32(pubkeyhash, prefix='bc')

        else:
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, "Please provide a seed phrase or public key.")
            return

        # Update the address entry with the imported address value
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, address)

        # Generate and display the QR code
        self.show_qr_code(address, self.qr_code_label)

        self.seed_phrase_import_entry.config(state="normal")
    
    def show_qr_code(self, address, label):
        # Generate the QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
        qr.add_data(address)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert the QR code image to a PhotoImage
        qr_code_image = ImageTk.PhotoImage(img)

        # Update the QR code label
        label.config(image=qr_code_image)
        label.image = qr_code_image

    def check_transactions(self):
        # Get the address value from the input field
        address = self.address_entry.get()

        # Check the last 3 transactions for a bitcoin address using the blockchain.com API
        url = f"https://blockchain.info/rawaddr/{address}"
        response = requests.get(url)

        if response.status_code == 200:
            transactions = []

            # Parse the transaction data from the API response
            data = response.json()
            for tx in data['txs'][:3]:
                tx_hash = tx['hash']
                tx_value = sum([o['value'] for o in tx['out'] if o['addr'] == address])
                transactions.append((tx_hash, tx_value))

            # Update the transactions value label with the result
            self.transactions_value.config(text=str(transactions))

            # Generate the QR code for the address
            self.show_qr_code(address, self.qr_code_label_transactions)
        else:
            self.transactions_value.config(text="Error checking transactions")


if __name__ == "__main__":
    root = ThemedTk(theme="radiance")  # You can choose other themes like "radiance", "breeze", etc.
    BitcoinWalletGeneratorGUI(root)
    root.mainloop()


