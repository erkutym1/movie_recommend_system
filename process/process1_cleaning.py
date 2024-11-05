import os
import pandas as pd

#dosyalari belirle
input_folder = 'movie_lens_20m'
output_folder = 'new_dataset'

#new dataset icin yol yoksa olustur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#her dosyadan timestamp temizle
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        input_file_path = os.path.join(input_folder, file_name)

        df = pd.read_csv(input_file_path)

        if 'timestamp' in df.columns:
            df = df.drop(columns=['timestamp'])

        output_file_path = os.path.join(output_folder, file_name)

        df.to_csv(output_file_path, index=False)
        print(f'{file_name} dosyası temizlendi')

