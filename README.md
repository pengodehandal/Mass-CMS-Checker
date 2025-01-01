# CMS CHECKER V1 🚀

## 📜 Deskripsi
Tools ini adalah alat untuk mengecek **CMS (Content Management System)** yang digunakan oleh website. Dengan tools ini, kamu bisa tau apakah suatu website menggunakan **WordPress**, **Joomla**, **Magento**, **Drupal**, **PrestaShop**, **Laravel**, dan banyak CMS lainnya.

Jadi, bagi lo yang suka ngecek CMS website atau sekedar pengen tau CMS apa yang dipake, ini dia tools yang lo cari! 😎🔥  
Biar makin keren, langsung aja cek website-website lo dan temukan CMS-nya! 💻🌐

---

### Penjelasan Fitur:

- **🔍 Deteksi CMS Beragam**: Tools ini mampu mendeteksi berbagai jenis CMS yang sangat populer dan digunakan banyak website, seperti **WordPress**, **Joomla**, **Magento**, **Drupal**, **PrestaShop**, **Laravel**, dan banyak lainnya. 💥
- **⚡ Multi-threading untuk Kecepatan**: Dengan dukungan multi-threading, pengecekan terhadap banyak website akan jauh lebih cepat. Ini sangat berguna ketika kamu punya daftar website yang panjang.
- **🛠️ Deteksi Path CMS Secara Otomatis**: Setiap CMS memiliki path tertentu yang dapat membantu tools ini untuk mendeteksi CMS tersebut, misalnya WordPress punya `/wp-content/`, Joomla punya `/administrator/`, dan seterusnya.
- **💾 Simpan Hasil ke File**: Semua website yang terdeteksi CMS-nya akan otomatis disimpan ke dalam file teks yang terpisah sesuai dengan CMS-nya (misalnya `wordpress.txt`).
- **🚫 Auto Remove Duplicate**: Duplikasi website dalam hasil deteksi otomatis dihindari, sehingga tidak ada data yang duplikat di dalam file output.
- **⏱️ Timeout Error Handling**: Jika website tidak merespon dalam 3 detik, maka tools ini akan otomatis melewati website tersebut dan melanjutkan pengecekan ke website berikutnya tanpa hang atau stuck.
- **📋 Output yang Jelas dan Rapi**: Hasil dari pengecekan CMS akan ditampilkan di console dan juga disimpan di file teks untuk setiap CMS yang terdeteksi. File tersebut disesuaikan dengan nama CMS, seperti `wordpress.txt`, `joomla.txt`, dan seterusnya.

---

## 🚀 Cara Penggunaan
   ```bash
   git clone https://github.com/pengodehandal/Mass-CMS-Checker/
   cd Mass-CMS-Checker
   pip install -r requirements.txt
   python3 checker.py
