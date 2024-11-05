import os
import pandas as pd
from tqdm import tqdm  # İlerleme çubuğu için

# Dosya yolları ve giriş dosyaları
genres_file = '../outputs/process3_genres_all.csv'
movies_file = '../new_dataset/movie.csv'
genome_scores_file = '../new_dataset/genome_scores.csv'
genome_tags_file = '../new_dataset/genome_tags.csv'

# Okuma işlemleri
genres_df = pd.read_csv(genres_file, header=None, names=['genre'])
movies_df = pd.read_csv(movies_file, usecols=['movieId', 'title', 'genres'], dtype={'movieId': 'int32'})
genome_scores_df = pd.read_csv(genome_scores_file, dtype={'movieId': 'int32', 'tagId': 'int32', 'relevance': 'float32'})
genome_tags_df = pd.read_csv(genome_tags_file, dtype={'tagId': 'int32', 'tag': 'string'})

# Genome skorlarını tag isimleriyle birleştirme
genome_merged_df = genome_scores_df.merge(genome_tags_df, on='tagId', how='left')

# Çıktı klasörünü oluştur
output_path = '../outputs/process8'
os.makedirs(output_path, exist_ok=True)

# Her bir genre için film-tag eşleşmelerini dosyalara yaz
for genre in tqdm(genres_df['genre'], desc="Tür dosyaları oluşturuluyor"):
    # Genre filtresi ile ilgili filmleri al
    genre_movies = movies_df[movies_df['genres'].str.contains(genre, na=False)]
    genre_output = []

    # Her film için tag bilgilerini alma
    for _, movie in genre_movies.iterrows():
        # Belirli bir film için tagleri relevance değeriyle filtreleyerek al (relevance >= 0.1 olanlar)
        movie_tags = genome_merged_df[
            (genome_merged_df['movieId'] == movie['movieId']) & (genome_merged_df['relevance'] >= 0.5)]

        # Film için mevcut tagleri "tag^relevance" formatında birleştir
        tags_str = ", ".join([f"{row['tag']}^{row['relevance']:.2f}" for _, row in movie_tags.iterrows()])
        genre_output.append([movie['title'], tags_str])

    # Sonuçları ilgili genre dosyasına yazma
    genre_df = pd.DataFrame(genre_output, columns=['movie', 'tags'])
    genre_df.to_csv(f'{output_path}/{genre}.csv', index=False)

# İşlem tamamlandı, her genre için ilgili dosya oluşturuldu.
print('Genre bazlı film ve tag dosyaları başarıyla oluşturuldu.')
