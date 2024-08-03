import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

def get_news():
    url = "https://www.alcircle.com/news/aluminium"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for article in soup.find_all('div', class_='listing-content'):
        title = article.find('h2').text
        summary = article.find('p').text
        date_str = article.find('span', class_='date').text
        date = datetime.strptime(date_str, '%d %B, %Y')

        if datetime.now() - date <= timedelta(days=45):
            articles.append({
                'title': title,
                'summary': summary,
                'date': date_str
            })

    with open('news_data.json', 'w') as f:
        json.dump(articles, f)

if __name__ == "__main__":
    get_news()
