import os
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

# Dosya yolları
user_interest_path = '../outputs/user_interest_scores'
genre_path = '../outputs/process8'
output_path = '../outputs/process9'

# Çıktı klasörünü oluştur
os.makedirs(output_path, exist_ok=True)

# Kullanılacak işlem sayısını %80 olarak ayarla
max_workers = max(1, int(multiprocessing.cpu_count() * 0.5))

# Kullanıcı bazlı öneri hesaplama fonksiyonu
def generate_recommendations(user_file):
    # Kullanıcı ID'sini dosya adından çıkar
    user_id = int(user_file.split("_")[1])

    # Kullanıcının ilgi puanlarını içeren dosyayı yükle
    user_interest_df = pd.read_csv(os.path.join(user_interest_path, user_file))
    user_interest_dict = dict(zip(user_interest_df['tag'], user_interest_df['interest_score']))

    recommendations = []

    # Her bir genre dosyasında işlem yap
    for genre_file in os.listdir(genre_path):
        genre = os.path.splitext(genre_file)[0]
        genre_df = pd.read_csv(f"{genre_path}/{genre_file}")

        genre_recommendations = []

        # İzlenmemiş her film için öneri puanı hesapla
        for _, row in genre_df.iterrows():
            movie = row['movie']
            tags_with_relevance = str(row['tags']) if pd.notna(row['tags']) else ""

            # Kullanıcının izlemediği filmler için puan hesapla
            recommend_score = 0
            for tag_relevance in tags_with_relevance.split(", "):
                if "^" in tag_relevance:
                    tag, relevance = tag_relevance.split("^")
                    relevance = float(relevance)

                    if tag in user_interest_dict:
                        # Öneri puanına ilgi puanı * relevance katkısı ekle
                        recommend_score += user_interest_dict[tag] * relevance

            # Eğer puan hesaplanmışsa, listeye ekle
            if recommend_score > 0:
                genre_recommendations.append((genre, movie, recommend_score))

        # Bu genre için en yüksek puanlı 15 filmi seç
        genre_recommendations = sorted(genre_recommendations, key=lambda x: x[2], reverse=True)[:15]
        recommendations.extend(genre_recommendations)

    # Önerileri dosyaya kaydet
    if recommendations:
        user_recommend_df = pd.DataFrame(recommendations, columns=['genre', 'movie', 'recommend_score'])
        user_recommend_df.to_csv(f"{output_path}/user_{user_id}_recommend_scores.csv", index=False)

# Ana fonksiyon
if __name__ == '__main__':
    # Kullanıcı dosyalarını al
    user_files = [f for f in os.listdir(user_interest_path) if f.startswith("user_") and f.endswith("_interest_scores.csv")]

    # Paralel işlemle kullanıcı önerilerini oluşturma
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(generate_recommendations, user_file) for user_file in user_files]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Kullanıcı bazlı öneriler oluşturuluyor"):
            future.result()  # Her bir işlem tamamlandığında sonucu al

    print("Tüm kullanıcılar için öneri dosyaları başarıyla oluşturuldu.")
