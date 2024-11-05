import pandas as pd
import os

# Dosya yolları
genres_file_path = '../outputs/process3_genres10.csv'
movie_file_path = '../new_dataset/movie.csv'
rating_file_path = '../new_dataset/rating.csv'
output_folder = 'outputs'
top50_output_path = os.path.join(output_folder, 'process4_top50.csv')

# Output klasörünü kontrol et ve oluştur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 1. genres10.csv dosyasından 10 kategori al
# İlk satırı atla, sadece gerçek kategorileri al
genres_df = pd.read_csv(genres_file_path, header=None, skiprows=1)
top_genres = genres_df[0].tolist()

# 2. movie.csv dosyasından belirtilen kategorilere göre filmleri bul
movies_df = pd.read_csv(movie_file_path, usecols=['movieId', 'title', 'genres'])

# 3. rating.csv dosyasını kullanarak en çok izlenen ve beğenilen filmleri bul
ratings_df = pd.read_csv(rating_file_path, usecols=['userId', 'movieId', 'rating'])

# Rating değeri 3.5 ve üzeri olanları filtrele
liked_ratings_df = ratings_df[ratings_df['rating'] >= 3.5]

# Her kategori için en çok izlenen ve beğenilen 50 filmi bul
top_movies_list = []
for genre in top_genres:
    # Belirtilen kategoriye göre filmleri filtrele
    genre_movies = movies_df[movies_df['genres'].str.contains(genre, na=False)]

    # Genre'deki filmlerden rating'i 3.5 ve üstü olanları bul
    genre_liked_movies = liked_ratings_df[liked_ratings_df['movieId'].isin(genre_movies['movieId'])]

    # Beğenilen filmlerden en çok izlenenleri bul
    genre_top_movies_count = genre_liked_movies['movieId'].value_counts().nlargest(50).index.tolist()

    # Film isimlerini al
    genre_movies_top_titles = genre_movies[genre_movies['movieId'].isin(genre_top_movies_count)]['title'].tolist()

    # Kategoriyi ve en çok izlenen beğenilen filmleri listeye ekle
    top_movies_list.append([genre, ', '.join(genre_movies_top_titles)])

# DataFrame oluştur ve dosyaya kaydet
top_movies_df = pd.DataFrame(top_movies_list, columns=['Genre', 'Top 50 Movies'])
top_movies_df.to_csv(top50_output_path, index=False)

print(f'Her kategori için en çok izlenen ve beğenilen 50 film başarıyla oluşturuldu ve {top50_output_path} dosyasına kaydedildi.')
