from eth_account import Account
import os

# Mengaktifkan fitur generasi entropi aman di eth-account
Account.enable_unaudited_hdwallet_features()

def generate_wallets(total_wallets: int, filename: str = "accounts.txt"):
    print(f"🔄 Membuat {total_wallets} wallet baru...")
    
    # Membuka file accounts.txt dalam mode 'append' (menambahkan tanpa menghapus isi lama)
    with open(filename, "a") as file:
        for i in range(1, total_wallets + 1):
            # Membuat wallet EVM acak baru
            new_account = Account.create()
            
            # Mengambil Private Key dalam bentuk Hex String
            private_key = new_account.key.hex()
            address = new_account.address
            
            # Menuliskan HANYA Private Key ke file accounts.txt
            file.write(f"{private_key}\n")
            
            print(f"[{i}/{total_wallets}] Berhasil dibuat -> Address: {address[:6]}...{address[-4:]}")

    print(f"\n✅ Selesai! {total_wallets} Private Key telah disimpan secara aman di file '{filename}'.")

if __name__ == "__main__":
    try:
        # Masukkan jumlah wallet yang ingin kamu buat
        jumlah = int(input("Masukkan jumlah wallet yang ingin dibuat: "))
        if jumlah > 0:
            generate_wallets(jumlah)
        else:
            print("Jumlah harus lebih dari 0!")
    except ValueError:
        print("Masukkan angka yang valid!")
