import hashlib
import hashlib

from bitcoinlib.wallets import wallet_create_or_open_by_key

def import_wallet_from_mnemonic(mnemonic):
    key = HDKey.from_passphrase(mnemonic)
    wallet_id = hashlib.sha256(mnemonic.encode()).hexdigest()
    wallet = wallet_create_or_open_by_key(wallet_id, keys=key, network='bitcoin', witness_type='segwit')
    print("Imported wallet address:", wallet.get_key().address)
    return wallet
