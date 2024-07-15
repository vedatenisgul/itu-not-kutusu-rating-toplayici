import requests
from bs4 import BeautifulSoup
from convert_name import convert_name
import pandas as pd

def get_course_data(ders):
    first_part = ders[:3]
    url = f'https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS&derskodu={first_part}'

    try:
        page = requests.get(url)
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Sayfa alınamadı: {e}")
        return None

    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', class_="table table-bordered table-striped table-hover table-responsive")

    if table:
        rows = table.find_all('tr')
        for row in rows:
            for td in row.find_all('td'):
                td.string = td.text.replace('Ý', 'İ').replace('ð', 'ğ').replace('þ', 'ş').replace('Ý', 'İ').replace('Ð', 'Ğ').replace('Þ', 'Ş').replace('ý', 'ı')

        headers = [th.text.strip() for th in rows[0].find_all('td')]
        data = [[td.text.strip() for td in row.find_all('td')] for row in rows[1:]]

        headers = data[0]
        instructor_index = headers.index('Instructor')
        crn_index = headers.index('CRN')
        course_code_index = headers.index('Course Code')
        #day_index = headers.index('Day')
        #time_index = headers.index('Time')

        result = [
            {
                headers[instructor_index]: row[instructor_index].strip(),
                headers[crn_index]: row[crn_index].strip(),
                #headers[day_index]: row[day_index].strip(),
                #headers[time_index]: row[time_index].strip(),
                headers[course_code_index]: row[course_code_index].strip()
            }
            for row in data[1:]
            if len(row) > course_code_index and row[course_code_index] == ders
        ]

        df = pd.DataFrame(result)
        return df
    else:
        print("Tablo bulunamadı. Lütfen ders kodunu kontrol edin.")
        return None

def get_notkutusu_ratings(session, instructor):
    isim = convert_name(instructor)
    url_notkutusu = f"http://www.notkutusu.com/lecturer/{isim}"
    score = 0
    try:
        lecturer_page = session.get(url_notkutusu)
        lecturer_page.raise_for_status()

        print(f"Successfully accessed {url_notkutusu}")
        soup = BeautifulSoup(lecturer_page.text, 'html.parser')
        ratings = {}

        for rate_id, label in zip(['rate-1', 'rate-3', 'rate-4', 'rate-5', 'rate-6'],
                                  ['Notu Bol mu?', 'Yardımseverlik', 'Ödev verir mi?', 'Yoklama alır mı?', 'Ders Anlatımı']):
            rate_div = soup.find(id=rate_id)
            rating_text = rate_div.text.strip() if rate_div else None

            if rating_text:
                try:
                    score += float(rating_text)
                except ValueError:
                    print(f"Could not convert rating '{rating_text}' to float for '{label}'")
            ratings[label] = rating_text

        if score != 0:
            ratings["Ortalama Score"] = round(score / 5,2)
        else:
            ratings["Ortalama Score"] = None

        return ratings

    except requests.exceptions.RequestException as e:
        print(f"Error accessing NotKutusu for {instructor}: {e}")
        return {}
