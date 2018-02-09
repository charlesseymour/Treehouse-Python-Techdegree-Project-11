from bisect import bisect

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
                                     RetrieveAPIView, UpdateAPIView,
                                     DestroyAPIView)
from rest_framework.response import Response

from . import serializers, models


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer
    
class RetrieveUpdateUserPref(RetrieveUpdateAPIView):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer
    
    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            user = self.request.user
        )
        
    def get(self, request):
        user_pref = self.get_object()
        serializer = serializers.UserPrefSerializer(user_pref)
        return Response(serializer.data)
        
    def put(self, request, format=None):
        data = request.data
        data['age'] = data['age'].split(',')
        data['gender'] = data['gender'].split(',')
        data['size'] = data['size'].split(',')
        try:
            user_pref = self.get_object()
            serializer = serializers.UserPrefSerializer(user_pref,
                                                        data=data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            serializer = serializers.UserPrefSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class GetUndecidedDog(APIView):
    def get(self, request, pk, format=None):
        user = self.request.user
        user_pref = models.UserPref.objects.get(user=user)
        preferred_dogs = models.Dog.objects.filter(
                               gender__in=user_pref.gender,
                               size__in=user_pref.size,
                               age_stage__in=user_pref.age
                               )
        liked_dogs = models.Dog.objects.filter(userdog__status__exact='l',
                                        userdog__user_id__exact=user.id)
        disliked_dogs = models.Dog.objects.filter(userdog__status__exact='d',
                                           userdog__user_id__exact=user.id)
        pk = int(pk)
        if pk == -1:
            undecided_dog = models.Dog.objects.exclude(id__in=liked_dogs).exclude(id__in=disliked_dogs).filter(id__in=preferred_dogs).first()
        else:
            undecided_dog = models.Dog.objects.exclude(id__in=liked_dogs).exclude(id__in=disliked_dogs).filter(id__in=preferred_dogs).filter(id__gt=pk).first()
        if not undecided_dog:
            raise Http404
        serializer = serializers.DogSerializer(undecided_dog)
        return Response(serializer.data)
        

class GetLikedDog(APIView):
    def get(self, request, pk, format=None):
        user = self.request.user
        liked_dogs = models.Dog.objects.filter(userdog__status__exact='l',
                                        userdog__user_id__exact=user.id)
        pk = int(pk)
        if pk == -1:
            liked_dog = liked_dogs.first()
        else:
            liked_dog = liked_dogs.filter(id__gt=pk).first()
        if not liked_dog:
            raise Http404
        serializer = serializers.DogSerializer(liked_dog)
        return Response(serializer.data)
        

class GetDislikedDog(APIView):
    def get(self, request, pk, format=None):
        user = self.request.user
        disliked_dogs = models.Dog.objects.filter(userdog__status__exact='d',
                                           userdog__user_id__exact=user.id)
        pk = int(pk)
        if pk == -1:
            disliked_dog = disliked_dogs.first()
        else:
            disliked_dog = disliked_dogs.filter(id__gt=pk).first()
        if not disliked_dog:
            raise Http404
        serializer = serializers.DogSerializer(disliked_dog)
        return Response(serializer.data)
        
class ReactToDog(UpdateAPIView):
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer
    
    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            user = self.request.user,
            dog = self.kwargs.get('pk')
        )
        
    def put(self, request, pk, reaction, format=None):
        reaction = 'l' if reaction == 'liked' else 'd' if reaction == 'disliked' else 'u'
        dog_id = pk
        user = self.request.user.id
        data = {'status': reaction, 'dog': dog_id, 'user': user}
        try:
            user_dog = self.get_object()
            if reaction == 'u':
                user_dog.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = serializers.UserDogSerializer(user_dog, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            serializer = serializers.UserDogSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''class MarkDogUndecided(DestroyAPIView):
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer'''
    
    
            
    
        
        
        
            
    
    
