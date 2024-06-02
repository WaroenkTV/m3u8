import requests
from bs4 import BeautifulSoup

def scrape_data():
    url = 'https://www.cubmu.com/play/live-tv?id=4028c68574537fcd0174be58644c5901&genreId=10'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data_element = soup.find('dt', id='dt-custom-data')
        if data_element:
            return data_element.get_text()
        else:
            return 'No data found'
    else:
        return 'Failed to fetch data'

if __name__ == "__main__":
    print(scrape_data())
