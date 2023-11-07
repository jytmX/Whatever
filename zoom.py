import ast

def get_sites_from_file(file_path):
    sites = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            dictionary = ast.literal_eval(line)
            site = dictionary.get('site')
            if site:
                sites.append(site)
    return sites

# Meminta nama file input
file_path = input("Masukkan nama file input: ")

# Memanggil fungsi get_sites_from_file() dengan file_path yang diberikan
site_list = get_sites_from_file(file_path)

# Meminta nama file output
output_file = input("Masukkan nama file output: ")

# Menyimpan hasil ke file output
with open(output_file, 'w') as file:
    for site in site_list:
        file.write(site + '\n')

print("Proses selesai. Hasil telah disimpan dalam file", output_file)
