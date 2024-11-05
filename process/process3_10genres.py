import pandas as pd
import os
from collections import Counter

# movie.csv dosyasını yükle
movies = pd.read_csv('../new_dataset/movie.csv', dtype={'movieId': 'int32'})

# Benzersiz türleri çıkar ve listeye dönüştür
unique_genres = set()
movies['genres'].dropna().apply(lambda x: unique_genres.update(x.split('|')))

# "no genres listed" değerini çıkar
unique_genres.discard("(no genres listed)")

# DataFrame oluştur ve genres.csv dosyasına kaydet
genres_df = pd.DataFrame(list(unique_genres))
genres_df.to_csv('outputs/process3_genres_all.csv', index=False, header=False)

print("Filtered unique genres başarıyla process3_genres_all.csv dosyasına yazdırıldı.")


ratings = pd.read_csv('../new_dataset/rating.csv', dtype={'userId': 'int32', 'movieId': 'int32'})

# Kategorilere göre en çok izlenen filmleri bulmak için gerekli birleştirme
movies_with_ratings = ratings.merge(movies, on='movieId')

# genres.csv dosyasını yükle
genres_df = pd.read_csv('../outputs/process3_genres_all.csv', header=None, names=['genre'])

# Sonuçları saklamak için boş bir liste oluştur
results = []

# Her tür için en çok izlenen 15 filmi bul
for genre in genres_df['genre']:
    # Eksik değerleri atla
    top_movies = (
        movies_with_ratings[movies_with_ratings['genres'].notna() & movies_with_ratings['genres'].str.contains(genre)]
        .nlargest(15, 'movieId')  # En çok izlenen 15 filmi al
    )
    for _, row in top_movies.iterrows():
        results.append({'genre': genre, 'movies': row['title']})

# DataFrame oluştur ve sonuçları CSV dosyasına kaydet
results_df = pd.DataFrame(results)
output_file = '../outputs/process3_top15_movies_by_genre.csv'
results_df.to_csv(output_file, index=False)

print(f"Her kategorideki en çok izlenen 15 film '{output_file}' dosyasına kaydedildi.")




movie_file_path = '../new_dataset/movie.csv'
output_folder = 'outputs'
output_file_path = os.path.join(output_folder, 'process3_genres10.csv')

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

movies_df = pd.read_csv(movie_file_path, usecols=['movieId', 'title', 'genres'])

all_genres = []

for genres in movies_df['genres']:
    if isinstance(genres, str):  # Sadece string olan değerleri kontrol et
        all_genres.extend(genres.split('|'))

genre_counts = Counter(all_genres)
top_10_genres = genre_counts.most_common(10)

top_10_genres_df = pd.DataFrame(top_10_genres, columns=['genre', 'count'])
top_10_genres_only = top_10_genres_df[['genre']]

top_10_genres_only.to_csv(output_file_path, index=False)

print(f'En çok tekrar eden 10 film türü başarıyla oluşturuldu ve {output_file_path} dosyasına kaydedildi.')
