import pandas as pd
from googletrans import Translator
import time

# --- PENGATURAN ---
# Nama file input Anda
input_filename = 'edgar_8k_summary_dataset.csv'
# Nama file output yang akan dihasilkan
output_filename = 'edgar_8k_summary_dataset_en.csv'
# Kolom yang akan diterjemahkan
column_to_translate = 'summary'
# Nama untuk kolom baru yang sudah diterjemahkan
new_column_name = 'summary_en'
# ------------------

# Inisialisasi penerjemah
translator = Translator()

# Baca file CSV
try:
    df = pd.read_csv(input_filename)
    print(f"✅ File '{input_filename}' berhasil dimuat. Memulai proses terjemahan...")
except FileNotFoundError:
    print(f"❌ ERROR: File '{input_filename}' tidak ditemukan. Mohon periksa nama dan lokasi file.")
    exit()

# Siapkan list untuk menampung hasil terjemahan
translated_texts = []
total_rows = len(df)

# Iterasi setiap baris dan terjemahkan teks di kolom yang ditentukan
for index, row in df.iterrows():
    text_to_translate = row[column_to_translate]
    
    # Coba terjemahkan, lakukan percobaan ulang jika gagal
    retries = 3
    for attempt in range(retries):
        try:
            if pd.notna(text_to_translate) and text_to_translate.strip() != "":
                translated = translator.translate(text_to_translate, src='id', dest='en')
                translated_texts.append(translated.text)
            else:
                translated_texts.append("") # Tambahkan string kosong jika sel asli kosong
            
            # Keluar dari loop percobaan jika berhasil
            break 
            
        except Exception as e:
            print(f"⚠️ Gagal menerjemahkan baris {index + 1}: {e}. Mencoba lagi dalam 5 detik... (Percobaan {attempt + 1}/{retries})")
            if attempt < retries - 1:
                time.sleep(5) # Tunggu sebelum mencoba lagi
            else:
                print(f"❌ Gagal total menerjemahkan baris {index + 1} setelah {retries} percobaan. Menambahkan teks kosong.")
                translated_texts.append("") # Gagal setelah semua percobaan

    # Tampilkan progres
    print(f"Menerjemahkan baris {index + 1}/{total_rows}...")

# Tambahkan hasil terjemahan sebagai kolom baru di DataFrame
df[new_column_name] = translated_texts

# Pilih kolom yang ingin disimpan di file baru (input asli dan summary terjemahan)
df_final = df[['input', new_column_name]]


# Simpan DataFrame baru ke file CSV
df_final.to_csv(output_filename, index=False, encoding='utf-8')

print(f"\n🎉 Proses selesai! Dataset yang sudah diterjemahkan disimpan sebagai '{output_filename}'.")