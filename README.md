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

# Jalankan allto1.py untuk mengirim aset OPbnb semua akun reff ke wallet master
```bash
python allto1.py
```

---

# Struktur Folder

```
SwarmBase-Bot/

├── main.py
├── generatePK.py
├── requirements.txt
├── accounts.txt
├── master_key.txt
├── allto1.py
└── README.md
```

### 🖥️ Contoh Output Terminal saat Dijalankan

Berikut adalah gambaran output visual di terminal (*command prompt*) ketika skrip dieksekusi:

```text
=== SwarmBase Auto Bot (Auto Sync Cooldown) ===

[ 10:15:02 ] | Master Wallet : 0x9A3f...B20a
[ 10:15:02 ] | Total Bot     : 2 Akun

[ 10:15:03 ] | === Akun [1] : 0x1A2b...3c4D ===
[ 10:15:04 ] | Saldo akun (0.000000 opBNB) kurang. Mengirim dari Master Wallet...
[ 10:15:09 ] | Refill Berhasil (+0.000003 opBNB)! TX: 0x8f7d9a1...c0e2
[ 10:15:10 ] | Saldo  : 0.000003 opBNB
[ 10:15:11 ] | Status : Belum Terdaftar. Melakukan Registrasi...
[ 10:15:16 ] | Registrasi Berhasil! TX: 0x3d4e5f6...a1b2
[ 10:15:17 ] | Proses : Melakukan Check-in Harian...
[ 10:15:21 ] | Check-in Berhasil! TX: 0x9e8d7c6...f5e4
[ 10:15:22 ] | NFT    : Mencoba Mint Pioneer Badge...
[ 10:15:27 ] | Mint Pioneer Berhasil! TX: 0x1a2b3c4...d5e6
--------------------------------------------------
[ 10:15:29 ] | === Akun [2] : 0x7E8f...9A0b ===
[ 10:15:30 ] | Saldo  : 0.000003 opBNB
[ 10:15:31 ] | Status : Sudah Terdaftar
[ 10:15:32 ] | Proses : Belum waktunya Check-in! Cooldown On-Chain: 00j 58m 12d
--------------------------------------------------
[ 10:15:34 ] | Siklus pemrosesan akun selesai.

[ Timer ] Menunggu check-in berikutnya dalam: 01:00:12
