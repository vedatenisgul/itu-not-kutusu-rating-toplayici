from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve email and password from environment variables
email = os.getenv('NOT_KUTUSU_EMAIL')
password = os.getenv('NOT_KUTUSU_PASSWORD')

def get_csrf_token(soup):
    token_input = soup.find('input', {'name': '_token'})
    return token_input['value'] if token_input else None

def login_not_kutusu(session):
    login_url = 'http://www.notkutusu.com/login'

    # Fetch the login page to obtain CSRF token
    login_page = session.get(login_url)
    login_page.raise_for_status()

    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = get_csrf_token(soup)

    if not csrf_token:
        raise RuntimeError("CSRF token not found. Unable to login.")

    # Perform login
    payload = {
        'email': email,
        'password': password,
        '_token': csrf_token
    }
    post = session.post(login_url, data=payload)
    post.raise_for_status()

    return session
