# 🚀 SwarmBase Auto Bot

Bot otomatis untuk SwarmBase di jaringan opBNB.

## Fitur main.py

- ✅ Multi Wallet
- ✅ Auto Register
- ✅ Auto Daily Check-in
- ✅ Auto Mint Pioneer Badge
- ✅ Auto Refill Gas dari Master Wallet
- ✅ Auto Cooldown On-Chain

## Fiture generatePK.py

- ✅ Membuat banyak wallet reff 

## Fitur allto1.py

- ✅ Mengirimkan semua aset OPbnb pada wallet reff ke wallet master

---

# Instalasi

Pastikan sudah menginstall **Python 3.10 atau lebih baru**.

```bash 
git clone https://github.com/erwindobp98/swarmbase.git
cd swarmbase
```

Install semua library:
```bash
pip install -r requirements.txt
```

---

#  Menambahkan Wallet atau Membuat Wallet reff

Buka file:

```
accounts.txt
```
Atau
```
nano accounts.txt
```
Isi satu Private Key per baris.

Contoh:

```
0xPrivateKey1
0xPrivateKey2
0xPrivateKey3
```
Simpan file setelah diubah atau tekan (ctrl+x+y+enter)

#  Atau buat baru automatis

Jalankan:

```bash
python generatePK.py
```

Masukkan jumlah wallet yang ingin dibuat.

Contoh:

```
100
```

Private Key akan otomatis tersimpan di:

```
accounts.txt
```

---

# Menyiapkan Master Wallet

Buka file:

```
master_key.txt
```
Atau
```
nano master_key.txt
```

Isi dengan **1 Private Key** wallet kusus menyimpan $opBNB.

Contoh:

```
0x123456789abcdef....
```
Simpan file setelah diubah atau tekan (ctrl+x+y+enter)

Master Wallet digunakan untuk mengirim saldo opBNB ke wallet/akun tuyul yang kekurangan gas.

> Pastikan Master Wallet memiliki saldo opBNB yang cukup.

---

# Mengganti Referral

Buka file:

```
main.py
```
Atau
```
nano main.py
```

Cari bagian berikut pada baris 32:

```python
self.CONTRACT_ADDRESS = {
    "core": "...",
    "nft": "...",
    "ref": "0x22f3185db0a560f9106d7c84d4a2ee0255a0aafd",
}
```

Ganti alamat pada bagian:

```python
"ref"
```

Misalnya:

```python
"ref": "0xAlamatReferralMilikAnda"
```

Contoh:

```python
self.CONTRACT_ADDRESS = {
    "core": "...",
    "nft": "...",
    "ref": "0x1234567890abcdef1234567890abcdef12345678",
}
```

Simpan file setelah diubah atau tekan (ctrl+x+y+enter)

> **Catatan:** Semua wallet yang belum pernah melakukan registrasi akan menggunakan alamat referral tersebut.

---

# Menjalankan Bot

Jalankan:

```bash
python main.py
```

Bot akan otomatis:

1. Membaca Master Wallet
2. Membaca semua wallet
3. Mengecek saldo
4. Mengirim gas jika diperlukan
5. Melakukan registrasi (jika belum)
6. Daily Check-in
7. Mint Pioneer Badge
8. Menunggu hingga waktu check-in berikutnya

# Mengganti Address wallet master

Buka file:

```
allto1.py
```
Atau
```
nano allto1.py
```

Cari bagian berikut pada baris 11:

```
DESTINATION_ADDRESS = "0x4b05CAD2a8E10DFdE15D0ec4239bCB94e107ccbC"
```

Ganti alamat pada bagian:

```python
DESTINATION_ADDRESS
```

Misalnya:

```python
DESTINATION_ADDRESS: "0xAlamatWalletMasterMilikAnda"
```

Contoh:

```python
DESTINATION_ADDRESS: "0x1234567890abcdef1234567890abcdef12345678"
```

Lalu jalankan untuk mengirim aset OPbnb semua akun reff ke wallet master

```bash
python allto1.py
```
