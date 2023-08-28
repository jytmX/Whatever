import json

# Buka file JSON
with open('pie.json') as file:
    data = json.load(file)

# Membuat list untuk menyimpan URL host
host_urls = []

# Loop melalui setiap baris dalam data
for item in data:
    # Mengambil nilai host dari setiap item
    host = item['host']
    
    # Menambahkan URL host ke dalam list
    host_urls.append(host)

# Menyimpan URL host ke dalam file teks
with open('host_urls.txt', 'w') as file:
    for url in host_urls:
        file.write(url + '\n')
