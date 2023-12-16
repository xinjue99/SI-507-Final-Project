from flask import Flask, render_template, request
import requests
import json
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

app = Flask(__name__)

class Film:
    """
    Represents a film with various attributes such as name, release year, etc.

    Attributes:
        name (str): The title of the film.
        release_year (int): The year the film was released.
        genres (list): A list of genres associated with the film.
        rating (float): The IMDb rating of the film.
        revenue (int): The box office revenue of the film.
        summary (str): A brief summary of the film.
        url (str): A URL to the film's IMDb page.
    """
    def __init__(self, name, release_year, genres, rating, revenue, summary, url):
        self.name = name
        self.release_year = release_year
        self.genres = genres
        self.rating = rating
        self.revenue = revenue
        self.summary = summary
        self.url = url


class TreeNode:
    """
    Represents a node in a tree structure.

    Attributes:
        value (any): The value contained in the node.
        descendants (list): A list of descendant nodes (children).
    """
    def __init__(self, value):
        self.value = value
        self.descendants = []

    def add_descendant(self, node):
        self.descendants.append(node)

def get_wiki_data(url):
    """
    Fetches and parses movie titles from Wikipedia tables.

    Parameters:
        url (str): The Wikipedia URL containing tables of movie titles.

    Returns:
        list: A list of movie titles extracted from the tables.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    movie_list = []
    for table in tables[:-1]:  
        df = pd.read_html(StringIO(str(table)))[0] 
        movie_list.extend(df.iloc[:, 1].dropna().tolist()) 
    return movie_list

def load_data_from_cache(file_path, titles):
    """
    Loads movie data from a cache file or retrieves it from an API if not found.

    Parameters:
        file_path (str): The path to the cache file.
        titles (list): A list of movie titles to retrieve data for.

    Returns:
        list: A list of movie data dictionaries.
    """
    try:
        with open(file_path, 'r') as cache:
            return json.load(cache)
    except FileNotFoundError:
        return retrieve_data_from_api(file_path, titles)

def retrieve_data_from_api(file_path, titles):
    """
    Retrieves data for given movie titles from the OMDB API and writes it to a cache file.

    Parameters:
        file_path (str): The path where the cached data will be stored.
        titles (list): A list of movie titles to retrieve data for.

    Returns:
        list: A list of dictionaries, each containing data about a movie.
    """
    api_key = "5efcb84b"
    base_url = f'http://www.omdbapi.com/?apikey={api_key}&t='
    movie_data = []
    for title in titles:
        query = title.lower().replace(' ', '+')
        response = requests.get(base_url + query)
        movie_data.append(response.json())
    with open(file_path, 'w') as cache:
        json.dump(movie_data, cache, indent=4)
    return movie_data

def process_data(movie_info):
    """
    Processes a list of movie data dictionaries, converting data types and adding URLs.

    Parameters:
        movie_info (list): A list of dictionaries with movie data.

    Returns:
        list: A list of Film objects with processed data.
    """
    films = []
    for movie in movie_info:
        movie['Title'] = str(movie.get('Title', ''))

        # Handle year conversion with potential range
        year = movie.get('Year', '0')
        movie['Year'] = int(year.split('–')[0]) if '–' in year else int(year)

        movie['Genre'] = movie.get('Genre', '').split(', ')

        # Handle 'N/A' in IMDb rating
        imdb_rating = movie.get('imdbRating', '0')
        movie['imdbRating'] = float(imdb_rating) if imdb_rating != 'N/A' else 0.0

        # Handle non-numeric box office values
        box_office = movie.get('BoxOffice', '0').replace('$', '').replace(',', '')
        movie['BoxOffice'] = int(box_office) if box_office.isdigit() else 0

        movie['Plot'] = str(movie.get('Plot', ''))

        imdb_id = movie.get('imdbID', '')
        movie_url = f'https://www.imdb.com/title/{imdb_id}/' if imdb_id else ''

        films.append(Film(movie['Title'], movie['Year'], movie['Genre'], 
                                    movie['imdbRating'], movie['BoxOffice'], 
                                    movie['Plot'], movie_url))

    return films

def find_duplicates(json_file):
    """
    Identifies duplicate movie titles in a JSON file.

    Parameters:
        json_file (str): The path to the JSON file containing movie data.

    Returns:
        list: A list of movie titles that appear more than once in the data.
    """
    with open(json_file, 'r') as file:
        data = json.load(file)
    titles = [m.get('Title', '') for m in data]
    return [t for t in titles if titles.count(t) > 1]

def recommend_movies(genre, rating_range, year_range, tree_root):
    """
    Recommends movies based on genre, IMDb rating range, and year range within a tree structure.

    Parameters:
        genre (str): The genre to filter movies by.
        rating_range (str): The IMDb rating range to filter movies by (e.g., '5-6').
        year_range (str): The release year range to filter movies by (e.g., '1990-2000').
        tree_root (TreeNode): The root node of the tree structure containing movie data.

    Returns:
        list: A list of Film objects that meet the filtering criteria.
    """
    genre_node = next((n for n in tree_root.descendants if n.value == genre), None)
    if not genre_node:
        return []

    rating_node = next((n for n in genre_node.descendants if n.value == rating_range), None)
    if not rating_node:
        return []

    year_node = next((n for n in rating_node.descendants if n.value == year_range), None)
    if not year_node:
        return []

    return [film for film in year_node.descendants]




