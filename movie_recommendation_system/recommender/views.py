import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MovieRecommendationView:
    def __init__(self):
        self.movies_data = pq.read_table('./static/movie_database.parquet').to_pandas()
        self.titles = self.movies_data['title'].to_list()

    def fetch_PosterLink_from_dictionary_from_imdb(self, imdb_id):
        try:
            link = f'https://www.omdbapi.com/?i={imdb_id}&apikey=c2433671'
            response = requests.get(link)
            response.raise_for_status()  # Check if the request was successful

            dictionary_data = response.json()  # Assuming the response is in JSON format
            poster_link = dictionary_data['Poster']
            return poster_link

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from the link: {e}")
            return None

    def get_recommendations(self, movie_id_from_db, movie_db):
        try:
            sim_scores = list(enumerate(movie_db[movie_id_from_db]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]  # get top 15 Recommendations

            movie_indices = [i[0] for i in sim_scores]
            output = self.movies_data.iloc[movie_indices]
            output.reset_index(inplace=True, drop=True)

            response = []
            for i in range(len(output)):
                response.append({
                    'image_url': self.fetch_PosterLink_from_dictionary_from_imdb(output['imdb_id'].iloc[i]),
                    'movie_title': output['title'].iloc[i],
                    'movie_release_date': output['release_date'].iloc[i],
                    'movie_director': output['main_director'].iloc[i],
                    'google_link': "https://www.google.com/search?q=" + '+'.join(output['title'].iloc[i].strip().split())
                })
            return response
        except Exception as e:
            logger.error(f"Error in get_recommendations: {e}")
            print("error: ", e)
            return []

    @method_decorator(login_required(login_url='u_login'))
    def render_index(self, request, input_provided='', movie_found='', recommendation_found='', recommended_movies=[],
                     input_movie_name=''):
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': self.titles,
                'input_provided': input_provided,
                'movie_found': movie_found,
                'recomendation_found': recommendation_found,
                'recommended_movies': recommended_movies,
                'input_movie_name': input_movie_name
            }
        )
    
    @method_decorator(login_required(login_url='u_login'))
    def home(self, request):
        if request.method == "GET":
            return self.render_index(request)

        if request.method == 'POST':
            data = request.POST
            movie_name = data.get('movie_name')

            if movie_name in self.titles:
                idx = self.titles.index(movie_name)
            else:
                logger.warning(f"Movie name not found: {movie_name}")
                return self.render_index(request, input_provided='yes', movie_found='', recommendation_found='',
                                         recommended_movies=[], input_movie_name=movie_name)

            model = pa.parquet.read_table('./static/model.parquet').to_pandas()
            final_recommendations = self.get_recommendations(idx, model)

            if final_recommendations:
                return render(
                    request,
                    'recommender/results.html',
                    {
                        'all_movie_names': self.titles,
                        'input_provided': 'yes',
                        'movie_found': 'yes',
                        'recomendation_found': 'yes',
                        'recommended_movies': final_recommendations,
                        'input_movie_name': movie_name
                    }
                )
            else:
                logger.warning(f"No recommendations found for movie: {movie_name}")
                return self.render_index(request, input_provided='yes', movie_found='', recommendation_found='',
                                         recommended_movies=[], input_movie_name=movie_name)


    def u_logout(self, request):
        logout(request)
        return redirect('home')

    def u_reg(self, request):
        if request.method == 'POST':
            u_name = request.POST.get('username')
            p_word = request.POST.get('password')
            f_name = request.POST.get('firstname')
            l_name = request.POST.get('lastname')
            e_mail = request.POST.get('email')

            if User.objects.filter(username=u_name).exists():
                logger.error(f"Username: {u_name} already exists!")
                return render(request, 'recommender/register.html', {'error': 'User already exists!'})

            user = User.objects.create(username=u_name, password=p_word, first_name=f_name, last_name=l_name, email=e_mail)
            user.save()
            
            return self.u_login(request, user)

        return render(request, 'recommender/register.html')

    def u_login(self, request, *user):
        if request.method == 'POST':
            u_name = request.POST['username']
            p_word = request.POST['password']
            
            try:
                user = User.objects.get(username=u_name, password=p_word)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                logger.error("Ivalid Credentials!")
                return render(request, 'recommender/login.html', {'error': 'Invalid credentials'})

        return render(request, 'recommender/login.html')
