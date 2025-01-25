from web3 import Web3
import time
import os
import random
from dotenv import load_dotenv
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

CHECK_MARK = Fore.GREEN + "✔️" + Style.RESET_ALL
CROSS_MARK = Fore.RED + "❌" + Style.RESET_ALL
BALANCE_SYMBOL = Fore.CYAN + "💰" + Style.RESET_ALL
ETH_SYMBOL = Fore.YELLOW + "Ξ" + Style.RESET_ALL
SENDER_ADDRESS_SYMBOL = Fore.CYAN + "📤 Alamat Pengirim:" + Style.RESET_ALL
RECEIVER_ADDRESS_SYMBOL = Fore.MAGENTA + "📥 Alamat Penerima:" + Style.RESET_ALL
AMOUNT_SYMBOL = Fore.LIGHTYELLOW_EX + "💵 Jumlah Kiriman:" + Style.RESET_ALL

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + "=" * 50)
    print(Fore.MAGENTA + " " * 10 + "THANKS")
    print(Fore.GREEN + " " * 10 + "BUY COFFEE FOR ME: 0x5ddA3d0d29ebC82a0f8baFe4091BCdA2b417C974 ")
    print(Fore.YELLOW + "=" * 50 + "\n")

load_dotenv()

# Ganti URL RPC untuk Hyperliquid EVM Testnet
web3 = Web3(Web3.HTTPProvider('https://api.hyperliquid-testnet.xyz/evm'))

if web3.is_connected():
    print(Fore.GREEN + f"Terkoneksi dengan jaringan Hyperliquid EVM Testnet {CHECK_MARK}")
else:
    print(Fore.RED + f"Gagal terhubung ke jaringan Hyperliquid EVM Testnet {CROSS_MARK}")
    raise Exception("Gagal terhubung ke jaringan Ethereum")

sender_address = os.getenv('SENDER_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

if not sender_address or not private_key:
    raise Exception(f"{CROSS_MARK} Harap isi SENDER_ADDRESS dan PRIVATE_KEY di file .env")

# Ganti fungsi generate_random_address dengan alamat penerima yang sudah ditentukan
receiver_address = "0x9436E82E06DE8Ff202C870dD9eEa22F56c5Ac25A"

def get_balance(address):
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')

def get_nonce():
    return web3.eth.get_transaction_count(sender_address)

def get_gas_price():
    return web3.eth.gas_price

def send_transaction(receiver_address, amount, gas_price):
    nonce = get_nonce()
    sender_balance_before = get_balance(sender_address)
    print(Fore.BLUE + f"{BALANCE_SYMBOL} Saldo Pengirim Sebelum Tx: {sender_balance_before:.18f} {ETH_SYMBOL}")
    print(Fore.CYAN + f"{SENDER_ADDRESS_SYMBOL} {sender_address}")
    print(Fore.MAGENTA + f"{RECEIVER_ADDRESS_SYMBOL} {receiver_address}")
    print(Fore.LIGHTYELLOW_EX + f"{AMOUNT_SYMBOL} {amount:.18f} {ETH_SYMBOL}")

    tx = {
        'nonce': nonce,
        'to': receiver_address,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': 998  # Sesuaikan chainId dengan Hyperliquid Testnet
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(Fore.CYAN + f"{datetime.now()} - Transaksi berhasil ke {receiver_address}. {CHECK_MARK}")
        
        sender_balance_after = get_balance(sender_address)
        print(Fore.YELLOW + f"{BALANCE_SYMBOL} Saldo Pengirim Setelah Tx: {sender_balance_after:.18f} {ETH_SYMBOL}")
        print(Fore.BLUE + f"{SENDER_ADDRESS_SYMBOL} {sender_address} {CHECK_MARK}")
        print(Fore.MAGENTA + f"{RECEIVER_ADDRESS_SYMBOL} {receiver_address} {CHECK_MARK}\n")

    except Exception as e:
        print(Fore.RED + f"Gagal mengirim transaksi: {str(e)} {CROSS_MARK}")

def countdown(seconds):
    while seconds:
        print(Fore.MAGENTA + f"Menunggu {seconds} detik untuk mencoba kembali...", end='\r')
        time.sleep(1)
        seconds -= 1
    print(Fore.GREEN + "Memulai kembali proses...\n")

while True:
    print_header()
    random_amount = random.uniform(0.0001, 0.0002)  # Jumlah transaksi acak
    gas_price = get_gas_price()
    send_transaction(receiver_address, random_amount, gas_price)
    countdown(30)
