def data_diri():
    simsul = {
        "Nama Lengkap": "Simsul Ramadhan",
        "Nama Panggilan": "Simsul",
        "Jenis Kelamin": "Laki-laki",
        "Tempat, Tgl Lahir": "Jakarta, 10 Mei 2003",
        "Alamat": "Jl. Merdeka No. 10, Jakarta",
        "Agama": "Islam",
        "Kewarganegaraan": "Indonesia",
        "Pendidikan": "Mahasiswa - Teknik Informatika",
        "Hobi": ["Membaca", "Menulis", "Programming"],
        "No. HP": "0812-3456-7890",
        "Email": "simsul@email.com"
    }

    print("==== DATA DIRI SIMSUL ====")
    for key, value in simsul.items():
        print(f"{key}: {value}")

data_diri()
