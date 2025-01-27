## Menyiapkan Lingkungan - Anaconda

Untuk membuat lingkungan pengembangan menggunakan Anaconda, ikuti langkah-langkah berikut:

1. Buat lingkungan baru dengan nama `main-ds` dan instal Python versi 3.9:
   ```conda create --name main-ds python=3.9```

2.  Aktifkan lingkungan yang telah dibuat
    ```conda activate main-ds```

3. Instal semua dependensi yang diperlukan dari file requirements.txt:
    ```pip install -r requirements.txt```  

## Menyiapkan Lingkungan - Shell/Terminal
Jika Anda menggunakan shell atau terminal, Anda dapat mengikuti langkah-langkah ini:

1. Buat direktori untuk proyek analisis data:

    ```mkdir proyek_analisis_data```

2. Masuk ke direktori proyek:

    ```cd proyek_analisis_data```

3. Instal Pipenv untuk mengelola lingkungan dan dependensi:
    ```pipenv install```

4. Aktifkan lingkungan Pipenv:
    ```pipenv shell```

5. Instal semua paket yang diperlukan dari file requirements.txt:
    ```pip install -r requirements.txt```

## Menjalankan Aplikasi Streamlit

Setelah menyiapkan lingkungan, jalankan aplikasi Streamlit dengan perintah berikut:
    ```streamlit run dashboard.py```
    
## Aplikasi akan terbuka di browser Anda, siap digunakan!

## Lisensi
Repository ini dilisensikan di bawah [MIT License](https://opensource.org/licenses/MIT).

## Penulis
- Nama: Raka Satria Efendi
- Email: [rakaefendi1683@gmail.com](mailto:rakaefendi1683@gmail.com)
- GitHub: [xurobaebae](https://github.com/xurobaebae)
- Instagram: [raka.fx](https://instagram.com/raka.fx)

Anda dapat mengganti `https://github.com/username/repo-name.git` dengan URL repository Anda yang sebenarnya. Juga, sesuaikan bagian "Penulis" jika Anda ingin menambahkan informasi lain. Selamat mengerjakan proyek Anda!
>>>>>>> ac2975149b2904b017c30b152222d6ac64599b6c
