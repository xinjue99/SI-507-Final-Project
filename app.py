from flask import Flask, render_template, request
from movie_recommender import recommend_movies, load_data_from_cache, get_wiki_data, process_data, Film, TreeNode
import humanize

app = Flask(__name__)

def initialize_data():
    """
    Initializes and processes the movie data from a Wikipedia page and a JSON cache file.
    It creates a tree structure where each genre is a parent node and each node contains
    children nodes of movies that fall into the corresponding genre, IMDb rating, and year range.

    Returns:
        tuple: A tuple containing a list of Film objects and the root node of the tree.
    """
    cache_file = 'movie_cache.json'
    wikiurl = 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture'
    movie_titles = get_wiki_data(wikiurl)
    raw_data = load_data_from_cache(cache_file, movie_titles)

    # Process the data
    processed_data = process_data(raw_data)

    films = processed_data

    # Build the tree structure
    all_genres = ['Mystery', 'Film-Noir', 'Sci-Fi', 'Western', 'Romance', 'Music', 'Animation', 'Thriller', 'Crime', 'History', 'Biography', 'Family', 'Adventure', 'Sport', 'Drama', 'Documentary', 'Action', 'Musical', 'Horror', 'Short', 'Comedy', 'War', 'Fantasy']
    imdb_rating_category = ['5-6', '6-7', '7-8', '8-9', '9-10']
    year_category = ['1920-1940', '1940-1960', '1960-1980', '1980-2000', '2000-2023']

    root = TreeNode('root')
    for genre in all_genres:
        genre_node = TreeNode(genre)
        root.add_descendant(genre_node)
        for rating in imdb_rating_category:
            rating_node = TreeNode(rating)
            genre_node.add_descendant(rating_node)
            for year in year_category:
                year_node = TreeNode(year)
                rating_node.add_descendant(year_node)
                for film in films:
                    if genre in film.genres and float(rating.split('-')[0]) <= film.rating <= float(rating.split('-')[1]) and int(year.split('-')[0]) <= film.release_year <= int(year.split('-')[1]):
                        year_node.add_descendant(film)

    return films, root

# Initialize data and tree structure
films, root = initialize_data()

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre']
    imdb_rating = request.form['imdb_rating']
    year_range = request.form['year_range']
    
    # Fetch recommendations based on the form data
    recommendations = recommend_movies(genre, imdb_rating, year_range, root)
    
    # Pass the recommendations to the template
    return render_template('recommendations.html', movies=recommendations)

@app.template_filter('currency')
def format_currency(value):
    return "${:,.2f}".format(value) if isinstance(value, (int, float)) else value

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
