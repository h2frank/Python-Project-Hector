import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_movie_details(movie_url):
    headers= {'User-Agent':	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    response = requests.get(movie_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Extract relevant information, modify as needed
        genre_list = soup.find_all('a', class_ = 'ipc-chip ipc-chip--on-baseAlt')
        genre = ""
        for element in genre_list:
            genre += element.find('span').text.strip() + ", "
        genre = genre[:-2]
        title = soup.find('h1').text.strip()
        rating = soup.find('span', class_ = 'sc-bde20123-1 cMEQkK').text.strip()

        return {'title': title, 'rating': rating, 'genre': genre}
    except:
        print('Error retrieving data')    

def scrape_imdb_top250(url):
    headers= {'User-Agent':	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the list of movies
    movie_list = soup.find_all('div', class_ = 'ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-c7e5f54-9 biraHx cli-title')

    # Create a dictionary to store movies
    movie_mapping = {}

    i=0
    for movie in movie_list:
        i+=1

        # Extract the movie URL
        movie_url = 'https://m.imdb.com' + movie.find('a')['href']
        movie_details = get_movie_details(movie_url)


        movie_mapping[i] = movie_details

    return movie_mapping

imdb_url = "https://m.imdb.com/chart/top/"

movies = scrape_imdb_top250(imdb_url)

# Print the results
df_movies = pd.DataFrame.from_dict(movies, orient='index')
print(df_movies.head())

df_movies.to_excel("top250IMDB.xlsx", index=False)