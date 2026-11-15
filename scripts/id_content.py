# Indonesian content for the GoNEST website. Numbers use Indonesian formatting (1.000 kg, Rp 2.900).

import content as K
PH = K.PHOTO_LABEL_ID  # photo key (also the file name) -> Indonesian label

CATS = K.CATS_ID

ROWS = K.ROWS_ID

STEPS = [
    ('1', 'Konsultasi', 'Kami meninjau konsep, target pasar, dan anggaran Anda.', 'Minggu 1'),
    ('2', 'Pengembangan', 'Draf formula dan pemilihan bahan baku.', 'Minggu 1 sampai 2'),
    ('3', 'Sampel', 'Anda mencicipi, kami menyesuaikan, Anda menyetujui.', 'Minggu 2 sampai 4'),
    ('4', 'Produksi', 'Produksi batch penuh sesuai formula yang disetujui.', 'Minggu 4 sampai 6'),
    ('5', 'Kontrol mutu', 'Pemeriksaan laboratorium dan pelepasan batch.', 'Minggu 6'),
    ('6', 'Pengiriman', 'Dikemas, dipalet, dan dikirim kepada Anda.', 'Minggu 6 sampai 8'),
]

PROJECTS = K.PROJECTS_ID

ARTICLES = K.ARTICLES_ID
CAT_ARTICLES = [a['cat'] for a in ARTICLES]

SERVICES = [
    dict(slug='pengembangan-produk', en_slug='product-development', name='Pengembangan Produk', lead='Konsep, formula, pemilihan bahan baku, dan putaran sampel sampai Anda menyetujui produknya.',
         over='Kami mengubah ide produk menjadi formula yang bisa diproduksi. Anda menyampaikan rasa, tekstur, kisaran harga, dan target pasar, lalu kami mengembangkan sampel sampai produk sesuai dengan brief Anda.',
         inc=['Pengembangan formula dan pemilihan bahan baku', 'Perkiraan biaya per unit', 'Putaran sampel dengan masukan tertulis', 'Sampel yang disetujui disimpan sebagai acuan produksi'],
         who=['Brand baru yang punya ide tetapi belum punya formula', 'Pemilik brand yang menambah lini produk', 'Distributor yang menambah merek sendiri'],
         steps=[('Brief', 'Anda menjelaskan produk dan membagikan acuan.'), ('Draf', 'Kami mengusulkan formula dan biaya.'), ('Sampel', 'Kami membuat sampel dan menyesuaikan sesuai masukan Anda.'), ('Persetujuan', 'Anda menyetujui satu sampel sebagai standar.')],
         photo='sample development',
         faqs=[('Berapa putaran sampel yang saya dapat?', 'Ketentuan sampel disepakati saat konsultasi. Dua sampai empat putaran adalah yang umum.'), ('Bisakah kalian meniru kompetitor?', 'Kami menyamakan target rasa dan tekstur, tetapi kami membuat formula sendiri dan tidak menyalin merek lain.'), ('Apakah formula yang saya biayai pengembangannya menjadi milik saya?', 'Itu tergantung model kerja sama. Kami menyepakatinya secara tertulis sebelum pengembangan dimulai.')]),
    dict(slug='jasa-maklon', en_slug='contract-manufacturing', name='Jasa Maklon', lead='Produksi sesuai spesifikasi dan formula yang sudah Anda setujui.',
         over='Anda membawa formula, atau menyetujui formula yang kami kembangkan, dan kami memproduksinya dalam jumlah yang Anda butuhkan dengan hasil yang sama setiap kali.',
         inc=['Produksi batch sesuai formula yang disetujui', 'Catatan batch dan sampel simpan', 'Pemeriksaan mutu sebelum pelepasan', 'Pengiriman sesuai jadwal'],
         who=['Brand yang sudah punya formula', 'Perusahaan yang mengalihdayakan sebagian produksinya', 'Brand yang naik skala dari produksi rumahan atau kecil'],
         steps=[('Pesanan', 'Konfirmasi jumlah, kemasan, dan tanggal pengiriman.'), ('Persiapan', 'Kami membeli bahan baku dan kemasan.'), ('Produksi', 'Kami menjalankan batch sesuai formula.'), ('Pelepasan', 'Pemeriksaan mutu, lalu pengiriman.')],
         photo='filling and sealing line',
         faqs=[('Berapa pesanan minimumnya?', 'Tergantung kategori. Lihat halaman Produk untuk angka contoh.'), ('Bisakah produksi dijadwalkan rutin?', 'Bisa. Pesanan ulang dapat direncanakan bulanan atau per kuartal.'), ('Bagaimana kalian menjaga konsistensi antar batch?', 'Batch ditimbang sesuai formula dan dibandingkan dengan sampel acuan yang disetujui.')]),
    dict(slug='private-label', en_slug='private-label', name='Private Label', lead='Formula siap pakai dari lini kami, dikemas dengan merek Anda untuk peluncuran yang lebih cepat dan murah.',
         over='Pilih formula dasar dari lini kami, sesuaikan rasa atau kemasannya, dan luncurkan dengan merek Anda tanpa membayar pengembangan penuh.',
         inc=['Pilihan formula dasar yang sudah ada', 'Penyesuaian rasa dan kemasan ringan', 'Label dan merek Anda', 'Pesanan minimum lebih rendah (ketentuan contoh)'],
         who=['Pengusaha pertama kali yang menguji pasar', 'Toko dan distributor yang menambah merek sendiri', 'Brand yang perlu meluncur cepat'],
         steps=[('Pilih', 'Pilih formula dasar dan cicipi.'), ('Sesuaikan', 'Pilih rasa dan ukuran kemasan.'), ('Merek', 'Kirim desain label Anda.'), ('Produksi', 'Kami memproduksi dan mengirim.')],
         photo='packaging options',
         faqs=[('Apakah merek lain akan menjual produk yang sama?', 'Formula dasar bisa dipakai bersama. Penyesuaian rasa dan kemasan membuat produk Anda berbeda, dan eksklusivitas bisa dibicarakan.'), ('Apakah minimumnya lebih rendah?', 'Biasanya ya, karena formulanya sudah dikembangkan.'), ('Secepat apa saya bisa meluncur?', 'Waktu contohnya 3 sampai 5 minggu, sebagian besar menunggu kemasan.')]),
    dict(slug='oem-odm', en_slug='oem-odm', name='OEM dan ODM', lead='OEM: kami memproduksi formula Anda. ODM: kami mengembangkan formulanya dan Anda memiliki mereknya.',
         over='OEM dan ODM menjelaskan siapa yang menciptakan produk. Pada OEM, Anda menyediakan spesifikasi dan kami memproduksinya. Pada ODM, kami merancang dan mengembangkan produk, dan Anda menjualnya dengan merek Anda.',
         inc=['OEM: produksi sesuai spesifikasi Anda', 'ODM: pengembangan ditambah produksi', 'Perjanjian tertulis tentang kepemilikan formula', 'Kerahasiaan formula dan merek Anda'],
         who=['Distributor dan pembeli B2B', 'Perusahaan yang punya spesifikasi produk sendiri', 'Brand yang ingin pengembangan dan produksi dari satu mitra'],
         steps=[('Pilih model', 'OEM, ODM, atau private label.'), ('Sepakati ketentuan', 'Kepemilikan, volume, dan harga.'), ('Kembangkan atau konfirmasi', 'Formula disetujui oleh Anda.'), ('Produksi', 'Batch dikirim sesuai jadwal.')],
         photo='client meeting',
         faqs=[('Apa beda OEM dan ODM?', 'OEM memproduksi rancangan Anda. ODM merancang dan memproduksi produk untuk Anda.'), ('Siapa pemilik formula pada ODM?', 'Kami menyepakatinya secara tertulis. Bisa eksklusif untuk Anda atau dibagi.'), ('Bisakah saya pindah ke pabrik lain nanti?', 'Pada OEM Anda memiliki spesifikasinya, jadi bisa. Pada ODM tergantung perjanjiannya.')]),
    dict(slug='kemasan', en_slug='packaging', name='Solusi Kemasan', lead='Saran format sachet, pouch, jar, dan boks, serta persyaratan label.',
         over='Kemasan memengaruhi masa simpan, biaya, dan daya tarik di rak. Kami membantu memilih bahan dan ukuran yang tepat, dan kami mengisi serta menyegel di pabrik sendiri.',
         inc=['Panduan bahan dan tingkat perlindungan', 'Rekomendasi berat neto dan ukuran', 'Pengisian dan penyegelan di pabrik sendiri', 'Pemeriksaan isi label sebelum dicetak'],
         who=['Brand yang belum yakin kemasan mana yang cocok', 'Pemilik yang mengubah ukuran atau format kemasan', 'Brand yang menyiapkan desain untuk pertama kali'],
         steps=[('Tinjau', 'Kami melihat produk dan pasarnya.'), ('Rekomendasi', 'Kami menyarankan format dan bahan.'), ('Desain', 'Desainer Anda menyiapkan label.'), ('Periksa', 'Kami memeriksa isi dan kecocokan sebelum dicetak.')],
         photo='packaging options',
         faqs=[('Apakah kalian menyediakan kemasan?', 'Kami bisa mencarikan kemasan dari pemasok kami, atau Anda menyediakan sendiri.'), ('Informasi apa yang wajib ada di label?', 'Kewajibannya tergantung produk dan peraturan. Kami mendaftar apa yang harus muncul dan Anda mengonfirmasinya ke regulator.'), ('Berapa minimum cetak kemasan?', 'Tergantung pemasoknya. Kami membagikan pilihannya saat konsultasi.')]),
]

STAGES = [
    ('Konsultasi Awal', 'Minggu 1', ['Meninjau konsep, target pasar, dan anggaran Anda', 'Menjelaskan pesanan minimum, jadwal, dan kisaran biaya'], ['Kirim brief singkat dan produk acuan jika ada', 'Sampaikan target harga dan ukuran pesanan pertama'], 'Brief proyek dan perkiraan penawaran'),
    ('Pengembangan Produk', 'Minggu 1 sampai 2', ['Menyusun draf formula dan memilih bahan baku', 'Memperkirakan biaya per unit'], ['Konfirmasi arah rasa dan anggaran'], 'Usulan formula'),
    ('Sampel dan Persetujuan', 'Minggu 2 sampai 4', ['Membuat sampel dan menyesuaikannya setelah tiap putaran', 'Mencatat formula yang disetujui'], ['Cicipi dan beri masukan yang jelas', 'Setujui sampel akhir secara tertulis'], 'Sampel yang disetujui, disimpan sebagai acuan produksi'),
    ('Produksi', 'Minggu 4 sampai 6', ['Membeli bahan baku dan kemasan', 'Menjadwalkan dan menjalankan batch sesuai formula yang disetujui'], ['Setujui desain kemasan', 'Konfirmasi jumlah pesanan dan ketentuan pembayaran'], 'Batch jadi, sudah dikemas'),
    ('Kontrol Mutu', 'Minggu 6', ['Memeriksa kadar air, berat, segel, dan rasa terhadap acuan', 'Melepas batch dan menyimpan sampel simpan'], ['Tinjau laporan batch jika diminta'], 'Laporan pelepasan batch'),
    ('Pengemasan dan Pengiriman', 'Minggu 6 sampai 8', ['Mengemas dalam karton, memalet, dan memberi label', 'Mengatur pengiriman atau serah terima untuk diambil'], ['Menerima dan memeriksa barang'], 'Surat jalan dan dokumen batch'),
]

FAC_AREAS = [('Penerimaan dan penyimpanan', 'receiving and storage', 'Bahan baku diperiksa, diberi label, dan disimpan menurut jenisnya.'),
             ('Ruang pencampuran kering', 'dry blending room', 'Serbuk dicampur menurut berat sesuai formula yang disetujui.'),
             ('Lini pengisian dan penyegelan', 'filling and sealing line', 'Lini sachet dan pouch mengisi dengan berat neto yang ditetapkan.'),
             ('Area pengepakan', 'packing area', 'Barang jadi dimasukkan ke karton dan diberi label per batch.'),
             ('Laboratorium QC', 'qc laboratory', 'Pemeriksaan kadar air, berat, dan sensori dilakukan di sini.'),
             ('Gudang barang jadi', 'finished goods warehouse', 'Batch menunggu pelepasan dan pengambilan.')]
