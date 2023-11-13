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
        #Limit to 10 movies per run
        i+=1
        if i ==11:
            break

        # Extract the movie URL
        movie_url = 'https://m.imdb.com' + movie.find('a')['href']
        movie_details = get_movie_details(movie_url)


        movie_mapping[i] = movie_details

    return movie_mapping

def genre_choice():
    
    initial_genre_n = input("Please, type the number of the genre that you want to watch based on the list below and hit \"Enter\":\n [1] Drama\n [2] Adventure\n [3] Thriller\n [4] Action\n [5] Crime\n [6] Comedy\n [7] Mystery\n [8] War\n [9] Fantasy\n [10] Romance\n [11] Family\n [12] Sci-Fi\n [13] Biography\n [14] Animation\n [15] History\n [16] Sport\n [17] Western\n [18] Music\n [19] Musical\n [20] Horror\n [21] Film-Noir\n")

    if initial_genre_n.isdigit():
        initial_genre_n = int(initial_genre_n)
        if initial_genre_n>0 and initial_genre_n<22:
            match initial_genre_n:
                case 1: 
                    initial_genre = 'Drama' 
                case 2: 
                    initial_genre = 'Adventure'
                case 3: 
                    initial_genre = 'Thriller'
                case 4: 
                    initial_genre = 'Action'
                case 5: 
                    initial_genre = 'Crime'
                case 6: 
                    initial_genre = 'Comedy'
                case 7: 
                    initial_genre = 'Mystery'
                case 8: 
                    initial_genre = 'War'
                case 9: 
                    initial_genre = 'Fantasy'
                case 10: 
                    initial_genre = 'Romance'
                case 11: 
                    initial_genre = 'Family'
                case 12: 
                    initial_genre = 'Sci-Fi'
                case 13: 
                    initial_genre = 'Biography'
                case 14: 
                    initial_genre = 'Animation'
                case 15: 
                    initial_genre = 'History'
                case 16: 
                    initial_genre = 'Sport'
                case 17: 
                    initial_genre = 'Western'
                case 18: 
                    initial_genre = 'Music'
                case 19: 
                    initial_genre = 'Musical'
                case 20: 
                    initial_genre = 'Horror'
                case 21: 
                    initial_genre = 'Film-Noir'

            print("Searching for top 10 " + initial_genre + " movies in the top 250 IMDB list...")

            return initial_genre
    
        else:
            return -1
    else:
        return -1


initial_genre = genre_choice()

if initial_genre != -1:
    imdb_url = "https://m.imdb.com/chart/top/?genres=" + str(initial_genre.lower())

    movies = scrape_imdb_top250(imdb_url)
    print(str(len(movies)) + "titles were found in the top 250 IMDB list, they are displayed down below:")

    # Print the results
    df_movies = pd.DataFrame.from_dict(movies, orient='index')
    print(df_movies)

    output_name = "top10IMDB_"+str(initial_genre.lower())+".xlsx"
    df_movies.to_excel(output_name, index=False)


else:
    print("The provided value is not accepted, try running the program again and following the instructions!")