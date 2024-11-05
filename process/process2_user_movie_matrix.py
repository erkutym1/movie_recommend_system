import pandas as pd
import os

# Dosya yolları
movie_file_path = '../new_dataset/movie.csv'
rating_file_path = '../new_dataset/rating.csv'

# Çıktı klasörü ve dosya yolları
output_folder = 'outputs'
user_movie_output_path = os.path.join(output_folder, 'process2_user_movie.csv')
user_movie_binary_output_path = os.path.join(output_folder, 'process2_user_movie_binary.csv')

# Çıktı klasörünü oluşturma
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# movie.csv ve rating.csv dosyalarını oku
movies_df = pd.read_csv(movie_file_path, usecols=['movieId', 'title'])
ratings_df = pd.read_csv(rating_file_path, usecols=['userId', 'movieId'])

# Film adlarıyla kullanıcı film ilişkisini birleştir
user_movie_df = pd.merge(ratings_df, movies_df, on='movieId')

# Tüm kullanıcılar için izledikleri filmleri listele ve kaydet
user_movie_agg = user_movie_df.groupby('userId')['title'].apply(lambda x: ', '.join(x)).reset_index()
user_movie_agg.columns = ['userId', 'movies']
user_movie_agg.to_csv(user_movie_output_path, index=False)

print(f'User-Movie tablosu başarıyla oluşturuldu ve {user_movie_output_path} dosyasına kaydedildi.')

# Kaç kullanıcı için binary tablo oluşturulacağını belirle
user_count_for_binary = 15

# İlk `user_count_for_binary` kadar kullanıcıyı seç
selected_users = user_movie_df['userId'].unique()[:user_count_for_binary]
user_movie_df_binary = user_movie_df[user_movie_df['userId'].isin(selected_users)]

# Kullanıcıların izlediği filmler için binary matrisi oluştur
user_movie_binary_df = pd.crosstab(user_movie_df_binary['title'], user_movie_df_binary['userId'])

# Crosstab sonucu zaten 1 ve 0 olarak gelir, bu yüzden ayrıca işlem yapmaya gerek yok
user_movie_binary_df = user_movie_binary_df.where(user_movie_binary_df > 0, 0)  # İzlemeyenler için 0

# Binary tabloyu kaydet
user_movie_binary_df.to_csv(user_movie_binary_output_path)

print(f'User-Movie binary tablosu başarıyla oluşturuldu ve {user_movie_binary_output_path} dosyasına kaydedildi.')
