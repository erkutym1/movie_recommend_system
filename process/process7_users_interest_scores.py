import os
import pandas as pd
import time

# Load data with optimized data types
movies = pd.read_csv('../new_dataset/movie.csv', dtype={'movieId': 'int32'})
ratings = pd.read_csv('../new_dataset/rating.csv', dtype={'userId': 'int32', 'movieId': 'int32'})
genome_scores = pd.read_csv('../new_dataset/genome_scores.csv', dtype={'movieId': 'int32', 'tagId': 'int32', 'relevance': 'float32'})
genome_tags = pd.read_csv('../new_dataset/genome_tags.csv', dtype={'tagId': 'int32'})

# Merge genome_scores with genome_tags
genome_scores = genome_scores.merge(genome_tags, on='tagId', how='left')

# Prepare the output directory for user interest scores
user_interest_dir = '../outputs/user_interest_scores'
os.makedirs(user_interest_dir, exist_ok=True)

# Get unique user IDs
user_ids = ratings['userId'].unique()

# Function to calculate and save tag interest scores for each user
def save_user_interest_scores(user_id):
    user_start_time = time.time()  # Kullanıcı işlem süresi başlangıcı

    # Kullanıcının izlediği filmleri al
    watched_movies = ratings[ratings['userId'] == user_id]
    watched_movie_ids = watched_movies['movieId'].tolist()

    # Kullanıcının kullandığı etiketlere göre ilgi puanlarını hesapla
    tag_relevance = genome_scores[genome_scores['movieId'].isin(watched_movie_ids)]
    tag_score = tag_relevance.groupby('tag')['relevance'].sum().reset_index()
    tag_score.columns = ['tag', 'interest_score']

    # Sonuçları bir CSV dosyasına kaydet
    tag_score.to_csv(f'{user_interest_dir}/user_{user_id}_interest_scores.csv', index=False)

    user_end_time = time.time()  # Kullanıcı işlem süresi bitişi
    print(f"User {user_id} için ilgi puanları kaydedildi. İşlem süresi: {user_end_time - user_start_time:.2f} saniye.")

# Tüm kullanıcılar için ilgi puanlarını hesapla ve kaydet
total_start_time = time.time()  # Toplam işlem süresi başlangıcı

for user_id in user_ids:
    save_user_interest_scores(user_id)

total_end_time = time.time()  # Toplam işlem süresi bitişi
print(f"Tüm kullanıcıların ilgi puanları kaydedildi. Toplam işlem süresi: {total_end_time - total_start_time:.2f} saniye.")
