import pandas as pd

#Reading the file we scraped from IMDB
movies_list = pd.read_excel("top250IMDB.xlsx")

#Getting all the available genres in the list
genres = movies_list.genre.str.split(",",expand=True).stack()
genres = genres.str.replace(" ", "")
genres = genres.unique()

#Getting input from user
print("Please, type the number of the genre that you want to watch based on the list below and hit \"Enter\":")

for ind, genre in enumerate(genres):
    print("["+str(ind)+"]", genre)

genre_n = input()

#Checking if input is number
if genre_n.isdigit():
    genre_n = int(genre_n)

    #Checking if input makes sense and providing output
    if genre_n > 0 and genre_n <len(genres):
        filter_mask = movies_list['genre'].str.contains(genres[genre_n])
        movies_filter = movies_list[filter_mask]
        movies_filter = movies_list.sort_values(by='rating', ascending=False).reset_index(drop=True)

        print("You selected the genre: " + genres[genre_n])

        print(movies_filter.head(10))

    else:
        print("The provided value is not accepted, try running the program again and following the instructions!")

else:
    print("The provided value is not accepted, try running the program again and following the instructions!")


