from api.models import Movie
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    '''
    Added decorator to rate_movie
    detail=True = Can only be applied to specific movie ...
    api/movies/1/rate_movie?
    pk = primary key/ the movie this method is being applied to.
    '''
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            print('movie title:', movie.title)
            user = request.user
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    '''
    Disable default update method. This will stop ratings
    being created/ updated
    '''
    
    def update(self, request, *args, **kwargs):
        response = {'message': 'You can\'t update a rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    '''
    Method override in views generally adds a record directly to the data
    and then returns a http response.
    Override default create method. Can't use api/ratings/1 POST/PUT
    Must use api/movies/1/rate_movie/
    '''

    def create(self, request, *args, **kwargs):
        response = {'message': 'You can\'t create a rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)