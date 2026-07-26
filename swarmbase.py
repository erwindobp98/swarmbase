from web3 import Web3, HTTPProvider
from web3.middleware import ExtraDataToPOAMiddleware
from web3.exceptions import TransactionNotFound
from eth_account import Account
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import asyncio, os, sys, time

# Inisialisasi colorama
init(autoreset=True)

class SwarmBaseAutoRefill:
    def __init__(self) -> None:
        self.API_URL = {
            "rpc": "https://opbnb-mainnet-rpc.bnbchain.org/",
            "explorer": "https://opbnbscan.com/tx/"
        }

        self.accounts = {}
        self.master_account = None

        # Pengaturan Nilai Transfer Pengisian Saldo
        self.MIN_BALANCE_THRESHOLD = 0.000001  # Batas minimal saldo opBNB sebelum di-refill
        self.REFILL_AMOUNT = 0.000003          # Jumlah opBNB yang dikirim jika saldo kurang

        # Durasi interval check-in standar (24 jam = 86400 detik)
        self.CHECKIN_INTERVAL = 24 * 3600 

        self.CONTRACT_ADDRESS = {
            "core": "0x01f9Eb284F94b54CF0854ef3B6FeF69C10babe0C",
            "nft": "0x6f7Cb024E5B285A9E7eE1b9D31e864e9d2B36627",
            "ref": "0x22f3185db0a560f9106d7c84d4a2ee0255a0aafd",
        }

        self.CORE_ABI = [
            {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "registered", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "referrer", "type": "address"}], "name": "registerWithReferral", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "swarmScore", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "lastHiveCheckIn", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "hiveStreak", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "totalCheckIns", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "hiveCheckIn", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "registrationTime", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
        ]

        self.NFT_ABI = [
            {"inputs": [], "name": "mintPioneer", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [], "name": "mintBuilder", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [], "name": "mintOG", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
            {"inputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}], "name": "hasBadge", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
            {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "totalMinted", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
        ]

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%X')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def load_master_account(self):
        filename = "master_key.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} tidak ditemukan. Silakan buat file ini dan isi dengan Private Key Master Wallet.{Style.RESET_ALL}")
                return False
            with open(filename, 'r') as file:
                key = file.read().strip()
                if not key:
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} kosong.{Style.RESET_ALL}")
                    return False
                keypair = Account.from_key(key)
                self.master_account = {
                    "keypair": keypair,
                    "address": keypair.address
                }
                return True
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Master Key Tidak Valid: {e}{Style.RESET_ALL}")
            return False

    def load_accounts(self):
        filename = "accounts.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} tidak ditemukan.{Style.RESET_ALL}")
                return []
            with open(filename, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Gagal memuat akun: {e}{Style.RESET_ALL}")
            return []

    def setup_account(self, idx: int, private_key: str):
        try:
            keypair = Account.from_key(private_key)
            self.accounts[idx] = {
                "keypair": keypair,
                "address": keypair.address
            }
            return True
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Private Key Index {idx} Tidak Valid: {e}{Style.RESET_ALL}")
            return False

    def mask_address(self, address):
        return f"{address[:6]}...{address[-4:]}"

    async def get_web3(self, retries=3, timeout=30):
        request_kwargs = {"timeout": timeout}
        for attempt in range(retries):
            try:
                provider = HTTPProvider(self.API_URL["rpc"], request_kwargs=request_kwargs)
                web3 = Web3(provider)
                web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
                await asyncio.to_thread(lambda: web3.eth.block_number)
                return web3
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                self.log(f"{Fore.RED + Style.BRIGHT}Gagal Konek ke RPC: {e}{Style.RESET_ALL}")
                return None

    async def get_balance(self, web3: Web3, address: str):
        try:
            checksum_addr = web3.to_checksum_address(address)
            balance = await asyncio.to_thread(web3.eth.get_balance, checksum_addr)
            return web3.from_wei(balance, "ether")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Gagal mengambil saldo: {e}{Style.RESET_ALL}")
            return 0

    async def send_raw_transaction(self, keypair, web3: Web3, tx: dict, retries=3):
        for attempt in range(retries):
            try:
                signed_tx = keypair.sign_transaction(tx)
                raw_tx = await asyncio.to_thread(
                    web3.eth.send_raw_transaction,
                    signed_tx.raw_transaction
                )
                return web3.to_hex(raw_tx)
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(f"{Fore.YELLOW + Style.BRIGHT}[Percobaan {attempt + 1}] TX Error: {e}{Style.RESET_ALL}")
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaksi gagal setelah mencapai maksimum percobaan.")

    async def wait_for_receipt(self, web3: Web3, tx_hash: str, retries=3):
        for attempt in range(retries):
            try:
                return await asyncio.to_thread(
                    web3.eth.wait_for_transaction_receipt,
                    tx_hash,
                    60
                )
            except Exception:
                await asyncio.sleep(2 ** attempt)
        raise Exception("Receipt tidak ditemukan.")

    async def refill_gas_if_needed(self, web3: Web3, target_address: str):
        target_balance = await self.get_balance(web3, target_address)
        
        if target_balance < self.MIN_BALANCE_THRESHOLD:
            self.log(f"{Fore.YELLOW + Style.BRIGHT}Saldo akun ({target_balance:.6f} opBNB) kurang. Mengirim dari Master Wallet...{Style.RESET_ALL}")
            
            master_keypair = self.master_account["keypair"]
            master_addr = web3.to_checksum_address(self.master_account["address"])
            master_bal = await self.get_balance(web3, master_addr)

            if master_bal < self.REFILL_AMOUNT:
                self.log(f"{Fore.RED + Style.BRIGHT}Master Wallet Kehabisan Saldo! ({master_bal:.6f} opBNB){Style.RESET_ALL}")
                return False

            latest_block = await asyncio.to_thread(web3.eth.get_block, "latest")
            base_fee = latest_block["baseFeePerGas"]
            max_priority_fee = web3.to_wei(0.001, "gwei")
            max_fee = base_fee + max_priority_fee
            nonce = await asyncio.to_thread(web3.eth.get_transaction_count, master_addr, "pending")
            chain_id = await asyncio.to_thread(lambda: web3.eth.chain_id)

            tx = {
                "from": master_addr,
                "to": web3.to_checksum_address(target_address),
                "value": web3.to_wei(self.REFILL_AMOUNT, "ether"),
                "gas": 21000,
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": nonce,
                "chainId": chain_id,
            }

            try:
                tx_hash = await self.send_raw_transaction(master_keypair, web3, tx)
                await self.wait_for_receipt(web3, tx_hash)
                self.log(f"{Fore.GREEN + Style.BRIGHT}Refill Berhasil (+{self.REFILL_AMOUNT} opBNB)! TX: {tx_hash}{Style.RESET_ALL}")
                return True
            except Exception as e:
                self.log(f"{Fore.RED + Style.BRIGHT}Gagal Refill dari Master Wallet: {e}{Style.RESET_ALL}")
                return False
        return True

    async def check_registered(self, idx: int, web3: Web3):
        try:
            address = web3.to_checksum_address(self.accounts[idx]['address'])
            contract = web3.eth.contract(
                address=web3.to_checksum_address(self.CONTRACT_ADDRESS["core"]),
                abi=self.CORE_ABI
            )
            return await asyncio.to_thread(contract.functions.registered(address).call)
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Gagal mengecek status registrasi: {e}{Style.RESET_ALL}")
            return None

    # --- FITUR BARU: CEK COOLDOWN DARI CONTRACT ---
    async def get_checkin_cooldown(self, idx: int, web3: Web3):
        """Mengecek sisa detik sebelum akun dapat melakukan check-in kembali berdasarkan data On-Chain."""
        try:
            address = web3.to_checksum_address(self.accounts[idx]['address'])
            contract = web3.eth.contract(
                address=web3.to_checksum_address(self.CONTRACT_ADDRESS["core"]),
                abi=self.CORE_ABI
            )
            
            last_checkin_time = await asyncio.to_thread(contract.functions.lastHiveCheckIn(address).call)
            
            # Jika belum pernah check-in
            if last_checkin_time == 0:
                return 0

            current_time = int(time.time())
            next_checkin_time = last_checkin_time + self.CHECKIN_INTERVAL
            time_left = next_checkin_time - current_time

            return max(0, time_left)
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Gagal membaca data cooldown: {e}{Style.RESET_ALL}")
            return 0

    async def perform_register(self, idx: int, web3: Web3):
        try:
            address = web3.to_checksum_address(self.accounts[idx]['address'])
            referrer = web3.to_checksum_address(self.CONTRACT_ADDRESS['ref'])
            contract = web3.eth.contract(
                address=web3.to_checksum_address(self.CONTRACT_ADDRESS["core"]),
                abi=self.CORE_ABI
            )
            function = contract.functions.registerWithReferral(referrer)
            
            estimated_gas = await asyncio.to_thread(function.estimate_gas, {"from": address})
            latest_block = await asyncio.to_thread(web3.eth.get_block, "latest")
            base_fee = latest_block["baseFeePerGas"]
            max_priority_fee = web3.to_wei(0.001, "gwei")
            max_fee = base_fee + max_priority_fee
            nonce = await asyncio.to_thread(web3.eth.get_transaction_count, address, "pending")
            chain_id = await asyncio.to_thread(lambda: web3.eth.chain_id)

            tx = await asyncio.to_thread(
                function.build_transaction,
                {
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": nonce,
                    "chainId": chain_id,
                }
            )

            tx_hash = await self.send_raw_transaction(self.accounts[idx]["keypair"], web3, tx)
            await self.wait_for_receipt(web3, tx_hash)
            return tx_hash
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Registrasi Gagal: {e}{Style.RESET_ALL}")
            return None

    async def perform_checkin(self, idx: int, web3: Web3):
        try:
            address = web3.to_checksum_address(self.accounts[idx]['address'])
            contract = web3.eth.contract(
                address=web3.to_checksum_address(self.CONTRACT_ADDRESS["core"]),
                abi=self.CORE_ABI
            )
            function = contract.functions.hiveCheckIn()

            estimated_gas = await asyncio.to_thread(function.estimate_gas, {"from": address})
            latest_block = await asyncio.to_thread(web3.eth.get_block, "latest")
            base_fee = latest_block["baseFeePerGas"]
            max_priority_fee = web3.to_wei(0.001, "gwei")
            max_fee = base_fee + max_priority_fee
            nonce = await asyncio.to_thread(web3.eth.get_transaction_count, address, "pending")
            chain_id = await asyncio.to_thread(lambda: web3.eth.chain_id)

            tx = await asyncio.to_thread(
                function.build_transaction,
                {
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": nonce,
                    "chainId": chain_id,
                }
            )

            tx_hash = await self.send_raw_transaction(self.accounts[idx]["keypair"], web3, tx)
            await self.wait_for_receipt(web3, tx_hash)
            return tx_hash
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Check-in Gagal: {e}{Style.RESET_ALL}")
            return None

    async def perform_mint_badge(self, idx: int, web3: Web3, badge_type: str):
        try:
            address = web3.to_checksum_address(self.accounts[idx]['address'])
            contract = web3.eth.contract(
                address=web3.to_checksum_address(self.CONTRACT_ADDRESS["nft"]),
                abi=self.NFT_ABI
            )
            
            if badge_type == "pioneer":
                function = contract.functions.mintPioneer()
            elif badge_type == "builder":
                function = contract.functions.mintBuilder()
            elif badge_type == "og":
                function = contract.functions.mintOG()
            else:
                return None

            estimated_gas = await asyncio.to_thread(function.estimate_gas, {"from": address})
            latest_block = await asyncio.to_thread(web3.eth.get_block, "latest")
            base_fee = latest_block["baseFeePerGas"]
            max_priority_fee = web3.to_wei(0.001, "gwei")
            max_fee = base_fee + max_priority_fee
            nonce = await asyncio.to_thread(web3.eth.get_transaction_count, address, "pending")
            chain_id = await asyncio.to_thread(lambda: web3.eth.chain_id)

            tx = await asyncio.to_thread(
                function.build_transaction,
                {
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": nonce,
                    "chainId": chain_id,
                }
            )

            tx_hash = await self.send_raw_transaction(self.accounts[idx]["keypair"], web3, tx)
            await self.wait_for_receipt(web3, tx_hash)
            return tx_hash
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Mint {badge_type.upper()} Badge Gagal: {e}{Style.RESET_ALL}")
            return None

    async def check_and_mint_badges(self, idx: int, web3: Web3):
        address = web3.to_checksum_address(self.accounts[idx]['address'])
        nft_contract = web3.eth.contract(
            address=web3.to_checksum_address(self.CONTRACT_ADDRESS["nft"]),
            abi=self.NFT_ABI
        )

        has_pioneer = await asyncio.to_thread(nft_contract.functions.hasBadge(address, 1).call)
        if not has_pioneer:
            self.log(f"NFT    : {Fore.YELLOW + Style.BRIGHT}Mencoba Mint Pioneer Badge...{Style.RESET_ALL}")
            pioneer_tx = await self.perform_mint_badge(idx, web3, "pioneer")
            if pioneer_tx:
                self.log(f"{Fore.GREEN + Style.BRIGHT}Mint Pioneer Berhasil! TX: {pioneer_tx}{Style.RESET_ALL}")

    async def process_single_account(self, idx: int):
        address = self.accounts[idx]['address']
        masked_addr = self.mask_address(address)
        self.log(f"{Fore.MAGENTA + Style.BRIGHT}=== Akun [{idx + 1}] : {masked_addr} ==={Style.RESET_ALL}")

        web3 = await self.get_web3()
        if not web3:
            return 0

        # 1. Refill Saldo jika diperlukan
        refill_status = await self.refill_gas_if_needed(web3, address)
        if not refill_status:
            self.log(f"{Fore.RED + Style.BRIGHT}Gagal memenuhi saldo minimum, melewati akun ini.{Style.RESET_ALL}")
            return 0

        curr_balance = await self.get_balance(web3, address)
        self.log(f"Saldo  : {Fore.GREEN + Style.BRIGHT}{curr_balance:.6f} opBNB{Style.RESET_ALL}")

        # 2. Check Registration
        is_registered = await self.check_registered(idx, web3)
        if is_registered is False:
            self.log(f"Status : {Fore.YELLOW + Style.BRIGHT}Belum Terdaftar. Melakukan Registrasi...{Style.RESET_ALL}")
            reg_tx = await self.perform_register(idx, web3)
            if reg_tx:
                self.log(f"{Fore.GREEN + Style.BRIGHT}Registrasi Berhasil! TX: {reg_tx}{Style.RESET_ALL}")
        else:
            self.log(f"Status : {Fore.GREEN + Style.BRIGHT}Sudah Terdaftar{Style.RESET_ALL}")

        # 3. Cek Cooldown Real-time sebelum Check-In
        cooldown_seconds = await self.get_checkin_cooldown(idx, web3)
        if cooldown_seconds > 0:
            hours, remainder = divmod(cooldown_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.log(f"Proses : {Fore.YELLOW + Style.BRIGHT}Belum waktunya Check-in! Cooldown On-Chain: {hours:02d}j {minutes:02d}m {seconds:02d}d{Style.RESET_ALL}")
        else:
            self.log(f"Proses : {Fore.WHITE + Style.BRIGHT}Melakukan Check-in Harian...{Style.RESET_ALL}")
            checkin_tx = await self.perform_checkin(idx, web3)
            if checkin_tx:
                self.log(f"{Fore.GREEN + Style.BRIGHT}Check-in Berhasil! TX: {checkin_tx}{Style.RESET_ALL}")
            
            # Re-fetch sisa cooldown setelah transaksi berhasil
            cooldown_seconds = await self.get_checkin_cooldown(idx, web3)

        # 4. Mint Badges
        await self.check_and_mint_badges(idx, web3)

        # Kembalikan sisa cooldown (plus buffer 2 menit ekstra)
        return cooldown_seconds + 120 if cooldown_seconds > 0 else (self.CHECKIN_INTERVAL + 120)

    async def countdown_timer(self, total_seconds: int):
        """Hitung mundur waktu tunggu secara langsung di terminal."""
        while total_seconds > 0:
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            timer_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            sys.stdout.write(
                f"\r{Fore.CYAN + Style.BRIGHT}[ Timer ]{Style.RESET_ALL} "
                f"{Fore.YELLOW + Style.BRIGHT}Menunggu check-in berikutnya dalam: {timer_str}{Style.RESET_ALL} "
            )
            sys.stdout.flush()
            await asyncio.sleep(1)
            total_seconds -= 1
        
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()

    async def run(self):
        while True:
            self.clear_terminal()
            print(f"{Fore.GREEN + Style.BRIGHT}=== SwarmBase Auto Bot (Auto Sync Cooldown) ===\n{Style.RESET_ALL}")
            
            if not self.load_master_account():
                return

            raw_accounts = self.load_accounts()
            if not raw_accounts:
                return

            master_addr = self.mask_address(self.master_account["address"])
            self.log(f"Master Wallet : {Fore.YELLOW + Style.BRIGHT}{master_addr}{Style.RESET_ALL}")
            self.log(f"Total Bot     : {Fore.WHITE + Style.BRIGHT}{len(raw_accounts)} Akun{Style.RESET_ALL}\n")

            min_cooldown_found = float('inf')

            for idx, pk in enumerate(raw_accounts):
                if self.setup_account(idx, pk):
                    next_wait = await self.process_single_account(idx)
                    
                    # Cari sisa cooldown terkecil di antara semua akun
                    if next_wait > 0 and next_wait < min_cooldown_found:
                        min_cooldown_found = next_wait
                        
                    print("-" * 50)
                    await asyncio.sleep(2)

            # Jika tidak ada cooldown yang terbaca, berikan delay default 24 jam + 2 menit
            if min_cooldown_found == float('inf') or min_cooldown_found <= 0:
                min_cooldown_found = self.CHECKIN_INTERVAL + 120

            self.log(f"{Fore.GREEN + Style.BRIGHT}Siklus pemrosesan akun selesai.{Style.RESET_ALL}")
            
            # Jalankan timer berdasarkan waktu tunggu riil terkecil
            await self.countdown_timer(int(min_cooldown_found))

if __name__ == "__main__":
    bot = SwarmBaseAutoRefill()
    asyncio.run(bot.run())
