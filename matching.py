import os
import pandas as pd

folder_input = "D:/10Q-Analyzer/datasets/EXTRACTED_FILLINGS_10Q(MDA)_TXT"  
folder_output = "D:/10Q-Analyzer/data-summary/SUMMARY_FILLINGS_10Q(MDA)_TXT"  
merge_csv_path = "D:/10Q-Analyzer/edgar_10Q_summary_dataset.csv" 

data_pairs = []

try:
    input_files = [f for f in os.listdir(folder_input) if f.endswith('.txt')]
    print(f"Ditemukan {len(input_files)} file di Folder A.")
except FileNotFoundError:
    print(f"ERROR: Folder A tidak ditemukan di '{folder_input}'. Mohon periksa kembali path Anda.")
    exit()


for filename in input_files:
    input_file_path = os.path.join(folder_input, filename)
    summary_file_path = os.path.join(folder_output, filename)

    if os.path.exists(summary_file_path):
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                input_text = f.read()

            with open(summary_file_path, 'r', encoding='utf-8') as f:
                summary_text = f.read()

            data_pairs.append({'input': input_text, 'summary': summary_text})

        except Exception as e:
            print(f"Gagal memproses file {filename}: {e}")

    else:
        print(f"Peringatan: File ringkasan '{filename}' tidak ditemukan di Folder B. Baris ini dilewati.")


if data_pairs:
    df = pd.DataFrame(data_pairs)

    df.to_csv(merge_csv_path, index=False, encoding='utf-8')
    print(f"Dataset berhasil dibuat dan disimpan di: {merge_csv_path}")
    print(f"Total {len(df)} pasang data berhasil diproses.")
else:
    print("\Tidak ada data yang berhasil diproses. Pastikan folder tidak kosong dan nama file cocok.")