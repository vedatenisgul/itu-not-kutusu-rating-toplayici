from get_data import get_course_data,get_notkutusu_ratings
from login import login_not_kutusu
from save_data_to_file import save_dataframe_to_csv
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import requests

# Main program flow
if __name__ == "__main__":
    ders = input("Please enter the course name: ").upper()
    df = get_course_data(ders)

    if df is not None and not df.empty:
        result = df.to_dict('records')

        with requests.Session() as session:
            session = login_not_kutusu(session)

            for entry in result:
                instructor = entry['Instructor']
                ratings = get_notkutusu_ratings(session, instructor)
                if not ratings:
                    ratings = {
                        'Notu Bol mu?': 'N/A',
                        'Yardımseverlik': 'N/A',
                        'Ödev verir mi?': 'N/A',
                        'Yoklama alır mı?': 'N/A',
                        'Ders Anlatımı': 'N/A',
                        'Ortalama Score': 0
                    }
                entry.update(ratings)
        df = pd.DataFrame(result)

        # Sort the DataFrame
        df_sorted = df.sort_values(by='Ortalama Score', ascending=False)
        df['Ortalama Score'] = df['Ortalama Score'].apply(lambda x: 'Bu isim Not Kutusu\'nda bulunmuyor' if pd.isna(x) else x)

        # save dataframe
        save_dataframe_to_csv(df_sorted)
    else:
        print("No instructor found.")


