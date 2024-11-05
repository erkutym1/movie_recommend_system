import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
import os

from mlxtend.preprocessing import TransactionEncoder
from tqdm import tqdm

# Dosya yolları
movie_file_path = '../new_dataset/movie.csv'
rating_file_path = '../new_dataset/rating.csv'
output_folder = 'outputs'
frequent_itemsets_output_path = os.path.join(output_folder, 'process5_sik_oge_kumeleri.csv')
association_rules_output_path = os.path.join(output_folder, 'process5_birliktelik_kurallari.csv')

# Output klasörünü kontrol et ve oluştur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 1. Filmleri ve ratingleri yükle
movies_df = pd.read_csv(movie_file_path, usecols=['movieId', 'title'])
ratings_df = pd.read_csv(rating_file_path, usecols=['userId', 'movieId'])

# 2. Kullanıcı-film ilişkilerini gruplandırarak bir liste oluştur
# Kullanıcıların izlediği film listesi
user_movie_list = ratings_df.groupby('userId')['movieId'].apply(list).tolist()

# 3. Transaction Encoder kullanarak verileri FPGrowth için uygun hale getir
# Her kullanıcı için izledikleri filmleri, ikili matris formatına çevireceğiz
# 3.1. Transaction listesi oluştur
transaction_list = []
for movies in tqdm(user_movie_list, desc="İşleniyor", unit="kullanıcı"):
    transaction = [str(movie) for movie in movies]  # movieId'leri string'e çevir
    transaction_list.append(transaction)

# 3.2. DataFrame formatına dönüştür
te = TransactionEncoder()
te_ary = te.fit(transaction_list).transform(transaction_list)
user_movie_matrix = pd.DataFrame(te_ary, columns=te.columns_)

# 4. Minimum destek oranını belirle ve sık öğe kümelerini hesapla
min_support = 0.1  # %40 destek oranı
frequent_itemsets = fpgrowth(user_movie_matrix, min_support=min_support, use_colnames=True)

# 5. Sık öğe kümelerini dosyaya kaydet
frequent_itemsets.to_csv(frequent_itemsets_output_path, index=False)
print(f'Sık öğe kümeleri başarıyla oluşturuldu ve {frequent_itemsets_output_path} dosyasına kaydedildi.')

# 6. Birliktelik kurallarını çıkar ve minimum güven değeri belirle
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

# 7. Birliktelik kuralları için Destek, Güven ve Lift değerlerini içeren bir DataFrame oluştur
rules_df = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
rules_df['antecedents'] = rules_df['antecedents'].apply(lambda x: ', '.join([str(item) for item in x]))
rules_df['consequents'] = rules_df['consequents'].apply(lambda x: ', '.join([str(item) for item in x]))

# Tablodaki başlıkları Türkçe yapalım
rules_df.columns = ['Ön Koşul (Antecedent)', 'Sonuç (Consequent)', 'Destek', 'Güven', 'Lift']

# 8. Birliktelik kurallarını dosyaya kaydet
rules_df.to_csv(association_rules_output_path, index=False)
print(f'Birliktelik kuralları başarıyla oluşturuldu ve {association_rules_output_path} dosyasına kaydedildi.')
