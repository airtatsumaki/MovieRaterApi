from api.models import Movie
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    '''
    Added decorator to rate_movie
    detail=True = Can only be applied to specific movie ...
    api/movies/1/rate_movie?
    pk = primary key
    '''
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            print('movie title:', movie.title)
            user = User.objects.get(id=1)
            print('user:', user)
            stars = request.data['stars']
            print('star rating:', stars)
            response = {'message': ''}
            try:
                rating = Rating.objects.get(movie=movie.id, user=user.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                '''
                Using a serializer can send the data in a readable format...
                easily compared to using a return string
                '''
                response = {'message': 'Rating UPDATED', 'result': serializer.data}
                #response['message'] = f'Rating UPDATED for {movie.title} to {stars} stars by {user.id}'
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(movie=movie, user=user, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating CREATED', 'result': serializer.data}
                #response['message'] = f'Rating UPDATED for {movie.title} to {stars} stars by {user.id}'
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'An error occured'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer