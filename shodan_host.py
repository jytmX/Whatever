import json

def extract_hostnames(input_file, output_file):
    # Membuka file JSON
    with open(input_file, 'r') as f:
        # Membaca setiap baris dalam file JSON
        lines = f.readlines()

    # Membuka file txt untuk menyimpan hasil ekstraksi
    with open(output_file, 'w') as f_out:
        # Memproses setiap baris JSON
        for line in lines:
            # Parsing JSON dari string
            data = json.loads(line)
            # Mengambil bagian hostnames
            hostnames = data.get('hostnames', [])
            # Menulis setiap hostname ke file output
            for hostname in hostnames:
                f_out.write(hostname + '\n')

if __name__ == "__main__":
    # Menanyakan nama file JSON yang akan diekstrak
    input_file = input("Masukkan nama file JSON yang akan diekstrak: ")
    # Menanyakan nama file output yang akan disimpan sebagai .txt
    output_file = input("Masukkan nama file untuk menyimpan hasil (dengan ekstensi .txt): ")
    # Menjalankan fungsi untuk ekstraksi
    extract_hostnames(input_file, output_file)
    print(f"Hostnames telah diekstrak dan disimpan di {output_file}")
