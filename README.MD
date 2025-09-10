Membuat sebuah README.md yang berisi tautan menuju aplikasi PWS yang sudah di-deploy, serta jawaban dari beberapa pertanyaan berikut.
- https://khayra-tazkiya-miufootballshop.pbp.cs.ui.ac.id/

- 1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
Jawaban : 
    1. membuat proyek django baru
    saya menyiapkan folder kerja, membuat lingkungan virtual (virtual environment), memasang django, lalu menjalankan perintah startproject. saya memakai underscore pada nama paket proyek karena nama paket harus berupa identifier python yang sah.

    mkdir miufootball-shop
    cd miufootball-shop
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install django
    python -m django startproject miufootball_shop .

    struktur awal:
    manage.py
    miufootball_shop/
    __init__.py
    settings.py
    urls.py
    wsgi.py
    asgi.py

    2. membuat aplikasi bernama main
    saya menambahkan aplikasi utama bernama main dan mendaftarkannya ke proyek.

    python manage.py startapp main
    aktifkan di miufootball_shop/settings.py:

    INSTALLED_APPS = [
        # aplikasi bawaan django …
        'main',
    ]

    3. routing proyek agar dapat menjalankan aplikasi main
    saya membuat berkas urls khusus untuk aplikasi main, lalu menghubungkannya dari urls proyek.


    main/urls.py:
    from django.urls import path
    from .views import home

    urlpatterns = [
        path("", home, name="home"),
    ]

    miufootball_shop/urls.py:
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("", include("main.urls")),
    ]


    4. membuat model product dengan 6 atribut wajib
    saya mendefinisikan model product sesuai ketentuan: name, price, description, thumbnail, category, is_featured.


    main/models.py:
    from django.db import models

    class Product(models.Model):
        name = models.CharField(max_length=100)
        price = models.IntegerField()
        description = models.TextField()
        thumbnail = models.URLField()
        category = models.CharField(max_length=50)
        is_featured = models.BooleanField(default=False)

        def __str__(self):
            return self.name

    5. membuat dan menerapkan migrasi basis data
    setiap perubahan pada model harus dimigrasikan agar skema basis data sesuai dengan kode.


    python manage.py makemigrations main
    python manage.py migrate

    6. membuat fungsi pada views.py dan templat html
    saya membuat fungsi home yang mengirim data nama aplikasi, nama saya, dan kelas ke templat. istilah “templat” mengikuti KBBI.


    main/views.py:
    from django.shortcuts import render

    def home(request):
        konteks = {
            "app_name": "Goalified FC Shop",  # ganti sesuai nama aplikasimu
            "name": "Nama Mahasiswa",
            "class_name": "Kelas PBP",
        }
        return render(request, "main.html", konteks)

    templat: letakkan di main/templates/main.html (perhatikan huruf besar/kecil karena server PWS peka terhadapnya).
    main/templates/main.html:
    <!DOCTYPE html>
    <html>
    <head>
        <title>MiuFootball Shop</title>
        <style>
            body {
            font-family: Comic Sans, Helvetica, sans-serif; 
            }
            h1 {
            font-family: "Courier New", monospace; 
            }
            h5 {
                font-family: "Courier New", monospace; 
                font-style: italic;            
            }
            p {
            font-size: 19px; 
            }
        </style>
    </head>
    <body>
        <h1>Welcome to {{ app_name }}!</h1>
        <h5>Gear up for glory—kits, boots, and pro training gear in one place.</h5>
        <p>Made by: {{ name }}</p>
        <p>Class: {{ class_name }}</p>
    </body>
    </html>

    7. memastikan routing urls.py aplikasi main ke fungsi pada views.py
    langkah ini sudah dilakukan pada butir 3 (path "" dipetakan ke fungsi home). jika halaman akar (/) belum mengarah ke home, pastikan include("main.urls") sudah ada di urls proyek.

    8. menguji secara lokal
    python manage.py runserver

    buka http://127.0.0.1:8000/ dan pastikan nama aplikasi, nama, serta kelas tampil.

    9. melakukan deployment ke pws
    saya menyiapkan variabel lingkungan (environment variable) untuk pws, menambahkan domain pws ke allowed_hosts, lalu mendorong (push) kode ke remote pws.


    pengaturan minimal di miufootball_shop/settings.py:
    import os
    from pathlib import Path
    from dotenv import load_dotenv

    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv()
    PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'

    if PRODUCTION:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DB_NAME'),
                'USER': os.getenv('DB_USER'),
                'PASSWORD': os.getenv('DB_PASSWORD'),
                'HOST': os.getenv('DB_HOST'),
                'PORT': os.getenv('DB_PORT'),
                'OPTIONS': {'options': f"-c search_path={os.getenv('SCHEMA','public')}"}
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "<username-sso>-<nama-proyek>.pbp.cs.ui.ac.id"]

    contoh .env (pengembangan lokal):
    PRODUCTION=False

    contoh .env.prod (untuk pws):
    DB_NAME=…
    DB_HOST=…
    DB_PORT=…
    DB_USER=…
    DB_PASSWORD=…
    SCHEMA= tugas_individu
    PRODUCTION=True

    langkah dorong ke pws (setelah menambahkan remote pws dari dasbor pws):
    git add .
    git commit -m "inisialisasi proyek, app main, model Product, view home"
    git push origin master
    git push pws master

    bila perlu jalankan perintah manajemen dari konsol pws:
    python manage.py migrate


2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
Jawaban:
    https://docs.google.com/document/d/1GNVq6tedFB3UAIGI46Pag97Xna98M94PoD7dfenFSe8/edit?usp=sharing

3. Jelaskan peran settings.py dalam proyek Django!
Jawaban:
    settings.py menyimpan konfigurasi global proyek Django: daftar aplikasi (INSTALLED_APPS), middleware, pengaturan database, template, static files, SECRET_KEY, DEBUG, ALLOWED_HOSTS, internationalization, time zone, hingga konfigurasi pihak ketiga. Intinya, ini “panel kontrol” proyek.

4. Bagaimana cara kerja migrasi database di Django?
Jawaban:
    1. Definisikan/ubah model di models.py.

    2. Jalankan python manage.py makemigrations → Django membaca perubahan model dan membuat berkas migrasi (skrip perubahan skema).

    3. Jalankan python manage.py migrate → menerapkan berkas migrasi ke database (membuat tabel/kolom/constraint).

    4. Django menjaga riwayat migrasi, sehingga kamu bisa melacak, menerapkan, atau rollback (ke versi tertentu) bila diperlukan.

5. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
Jawaban:
    - Productive & opinionated: banyak fitur bawaan (admin, ORM, auth, form) → cepat melihat hasil nyata.

    - Arsitektur jelas (MVT): memudahkan memahami pemisahan concern data–logika–presentasi.

    - Dokumentasi & ekosistem kuat: mudah dipelajari dan dibantu komunitas.

    - Aman & andal: proteksi XSS/CSRF/SQLi bawaan → praktik baik sejak awal.

    - Skalabel: dari tugas kuliah hingga aplikasi produksi serius—sekali belajar, manfaat panjang.


6. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
Jawaban: belum ada
