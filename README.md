<div align="center">

# 🎬 Movie Recommendation System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

A Content-Based Movie Recommendation System built with Django, powered by Scikit-Learn for Machine Learning and the OMDb API for live fetching of movie posters.
</div>

---

## 🌟 Features

- **Content-Based Filtering**: Recommends movies based on similarity using attributes like genre, keywords, cast, and director.
- **Interactive UI**: A clean and engaging frontend to search for and view movie recommendations.
- **User Authentication**: Secure Login, Registration, and Logout features via Django's built-in authentication system.
- **Live Poster Fetching**: Integrates with the [OMDb API](http://www.omdbapi.com/) to fetch high-quality movie posters in real-time.
- **Optimized Data Storage**: Uses Parquet files (`.parquet`) for lighting-fast data reading compared to traditional CSVs.

---

## 🛠️ Technologies Used

### Backend
- **Python**
- **Django** (Web Framework)

### Machine Learning & Data Processing
- **Pandas** & **NumPy**
- **Scikit-Learn** (Cosine Similarity, CountVectorizer)
- **NLTK** (Stemming)
- **PyArrow** / **FastParquet** (For efficient Parquet file storage)
- **Jupyter Notebook** (For model training and exploratory data analysis)

### Frontend
- **HTML / CSS**
- **jQuery UI** (For Autocomplete Search Suggestions)

### APIs
- **OMDb API** (For fetching poster links)

---

## 📂 Project Structure

```bash
.
├── Dataset/                     # Raw CSV data files
├── Python_Internship_Documentation.ipynb # Documentation & Python basic exercises
├── recommender.ipynb            # ML model building and training notebook
├── movie_recommendation_system/ # Django Project Directory
│   ├── movie_recommendation_system/ # Django configurations (settings, urls)
│   ├── recommender/             # Core Django App
│   │   ├── static/              # CSS files
│   │   ├── templates/           # HTML templates (login, register, index, results)
│   │   ├── views.py             # Core logic for handling requests, API calls & recommendations
│   │   ├── models.py            # Database models
│   │   └── urls.py              # App routing
│   └── manage.py                # Django CLI entry point
├── requirements.txt             # Project Dependencies
└── README.md                    # Project Documentation
```

---

## 🚀 Setup & Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/JindalChaitanya/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Build the Recommendation Model
The application relies on `.parquet` files for the pre-computed similarity matrix and movie metadata. You need to generate them first.
1. Download the required dataset (e.g., from Kaggle: The Movies Dataset) and place the CSV files (`movies_metadata.csv`, `keywords.csv`, etc.) in the `Dataset/` folder.
2. Open the Jupyter Notebook `recommender.ipynb`:
    ```bash
    jupyter notebook recommender.ipynb
    ```
3. Run all the cells in the notebook. This script cleans the data, engineers the features, calculates the cosine similarity, and outputs `movie_database.parquet` and `model.parquet`.
4. Move or copy the generated `.parquet` files to the Django static directory so the app can read them:
    ```bash
    mkdir -p movie_recommendation_system/static
    cp Dataset/movie_database.parquet movie_recommendation_system/static/
    cp Dataset/model.parquet movie_recommendation_system/static/
    ```

### 5. Run Django Migrations
Initialize the database for user authentication.
```bash
cd movie_recommendation_system
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser. Register an account, log in, and start exploring recommendations!

---

## 🧠 How the Recommendation Engine Works

1. **Data Preprocessing**: It merges `movies_metadata`, `credits`, and `keywords` datasets. It extracts important metadata (Director, Top Cast, Genres, Keywords).
2. **Text Processing**: All extracted text is converted to lowercase and stripped of spaces to treat full names as unique entities (e.g., "Johnny Depp" -> "johnnydepp"). NLTK is used for stemming words.
3. **Vectorization**: A `CountVectorizer` is used to create a matrix of token counts from the combined text "soup".
4. **Cosine Similarity**: We calculate the Cosine Similarity score between all movies based on their vectorized representation.
5. **Retrieval**: When a user selects a movie, the system looks up the top 10 movies with the highest similarity scores and returns them to the frontend.

---

## 🔑 OMDb API Key Configuration
By default, the application uses an API key hardcoded in `views.py`. If you exceed API limits or wish to use your own key:
1. Get a free API key from [OMDb API](http://www.omdbapi.com/apikey.aspx).
2. Open `movie_recommendation_system/recommender/views.py`.
3. Locate the `fetch_PosterLink_from_dictionary_from_imdb` method and replace the `apikey=...` parameter with your own key.

---

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).
