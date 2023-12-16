# Movie Recommender System

## Description
This project is a Flask-based web application that recommends movies to users based on their selected preferences such as genre, IMDb rating, and year range. It utilizes data fetched from the OMDb API and processed into a structured tree for efficient retrieval.

## Installation
To run this project, you will need the following packages:\
flask\
requests\
pandas\
io\
bs4\
lxml

## Usage
Download all the files in the repository, including two python files and two templates.\
First run movie_recommender.py then run app.py.\
Now you can navigate to http://127.0.0.1:5000/ in web browser to interact with the application.

## Data
### Data Sources
OMDb API: Movies information is fetched from the OMDb API.\
Wikipedia: The list of movies nominated for the Academy Award for Best Picture is scraped from Wikipedia.
### Data Caching
Data fetched from the OMDb API is cached in a JSON file to minimize repeated API calls and enhance performance.

### Data Structure
The data is organized into a tree structure with genres as parent nodes and movies as leaf nodes. This structure is stored in a .json file for persistence.

## Interactivity and Presentation
•	Visit the homepage and use the dropdown menus to select movie preferences.\
•	Click "Get Recommendations" to view a list of suggested movies.\
•	Each movie in the recommendation list includes a link to its IMDb page for further details.


## Special Instructions
API Keys: Obtain your own OMDB API key through https://www.omdbapi.com/apikey.aspx
## Files and Directories
app.py: The Flask application.\
movie_recommender.py: Contains the logic for fetching, processing, and structuring movie data.\
templates: HTML files for the web interface.\
movie_cache.json: Cached movie data.
