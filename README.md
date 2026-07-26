# 🐝 SwarmBase Auto Bot (opBNB Network)

Bot otomatisasi berbasis Python untuk melakukan registrasi, check-in harian, dan minting NFT Badge pada protokol **SwarmBase** di jaringan **opBNB Chain**, dilengkapi dengan fitur **Auto-Refill Gas Fee** dari Master Wallet serta **Auto-Sync Cooldown Real-Time**.

---

## 🌟 Fitur Utama

- **Auto Gas Refill:** Mengisi saldo opBNB secara otomatis ke akun bot dari Master Wallet jika saldo kurang dari batas minimum.
- **Real-Time On-Chain Cooldown Sync:** Membaca status cooldown `lastHiveCheckIn` langsung dari smart contract. Bot secara otomatis mendeteksi sisa waktu cooldown per akun secara akurat (tidak asal lewati atau eksekusi).
- **Smart Dynamic Timer:** Menghitung sisa cooldown terkecil dari seluruh akun dan memasang timer hitung mundur (*live countdown*) otomatis sebelum menjalankan siklus berikutnya.
- **Auto Registration:** Mendaftarkan akun ke SwarmBase dengan kode referral secara otomatis jika belum terdaftar.
- **Auto Daily Check-In:** Mengklaim poin harian (*Swarm Score*) hanya ketika cooldown akun sudah selesai, menghemat gas fee.
- **Auto Mint Badges:** Memeriksa kualifikasi dan melakukan minting Pioneer/Builder/OG Badge secara otomatis.

---

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
