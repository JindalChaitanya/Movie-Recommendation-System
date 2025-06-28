from django.urls import path
from .views import MovieRecommendationView

movie_recommender_view = MovieRecommendationView()


urlpatterns = [
    path('register/', movie_recommender_view.u_reg, name='u_reg'),
    path('login/', movie_recommender_view.u_login, name='u_login'),
    path('logout/', movie_recommender_view.u_logout, name='u_logout'),
    path('', movie_recommender_view.home, name='home'),
    # Add other URLs as needed
]
