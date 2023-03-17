import requests
from bitcoinlib.keys import Key

API_URL = "https://api.blockchair.com/bitcoin/dashboards/address/{}"

def get_address_from_public_key(public_key_hex):
    key = Key(import_key=public_key_hex)
    return key.address()

def get_balance(address):
    response = requests.get(API_URL.format(address))
    response_data = response.json()

    if response.status_code == 200 and "data" in response_data:
        balance = response_data["data"][address]["address"]["balance"]
        return balance
    else:
        raise Exception("Error fetching balance")

def main():
    public_key_hex = input("Enter your public key (hex format): ")
    address = get_address_from_public_key(public_key_hex)
    print(f"Bitcoin address: {address}")

    balance = get_balance(address)
    print(f"Wallet balance: {balance} satoshis")

if __name__ == '__main__':
    main()
