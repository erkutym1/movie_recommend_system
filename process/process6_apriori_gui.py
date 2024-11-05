import pandas as pd
import tkinter as tk
from tkinter import ttk
import os

# Dosya yolları
association_rules_output_path = '../outputs/process5_birliktelik_kurallari.csv'  # Process5 çıktısı

# Birliktelik kurallarını oku
rules_df = pd.read_csv(association_rules_output_path)

# Arayüz oluşturma
class FilmArayuzu:
    def __init__(self, master):
        self.master = master
        master.title("Film Birliktelik Kuralları")
        master.geometry("300x200")

        # Kural olan filmleri al
        self.film_list = pd.concat([rules_df['Ön Koşul (Antecedent)'], rules_df['Sonuç (Consequent)']]).unique().tolist()

        # Açılır menü 1
        self.label1 = tk.Label(master, text="Birinci Film Seçiniz:")
        self.label1.pack()
        self.combo_box1 = ttk.Combobox(master, values=self.film_list)
        self.combo_box1.pack()

        # Açılır menü 2
        self.label2 = tk.Label(master, text="İkinci Film Seçiniz:")
        self.label2.pack()
        self.combo_box2 = ttk.Combobox(master, values=self.film_list)
        self.combo_box2.pack()

        # Hesapla butonu
        self.hesapla_button = tk.Button(master, text="Hesapla", command=self.hesapla)
        self.hesapla_button.pack()

        # Sonuç label'ı
        self.sonuc_label = tk.Label(master, text="")
        self.sonuc_label.pack()

    def hesapla(self):
        # Seçilen filmleri al
        film1 = self.combo_box1.get()
        film2 = self.combo_box2.get()

        # Seçili filmler için kuralları bul
        rule = rules_df[(rules_df['Ön Koşul (Antecedent)'] == film1) & (rules_df['Sonuç (Consequent)'] == film2)]

        if not rule.empty:
            destek = rule['Destek'].values[0]
            guven = rule['Güven'].values[0]
            lift = rule['Lift'].values[0]
            sonuc = f"Destek: {destek:.2f}, Güven: {guven:.2f}, Lift: {lift:.2f}"
        else:
            sonuc = "Bu film kombinasyonu için kural bulunamadı."

        self.sonuc_label.config(text=sonuc)

# Ana uygulamayı başlat
root = tk.Tk()
film_arayuzu = FilmArayuzu(root)
root.mainloop()
