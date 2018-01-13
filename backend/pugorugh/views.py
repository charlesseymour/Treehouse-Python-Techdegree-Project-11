from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
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
        
    def put(self, request, format=None):
        user_pref = self.get_object()
        data = request.data
        data['age'] = data['age'].split(',')
        data['gender'] = data['gender'].split(',')
        data['size'] = data['size'].split(',')
        serializer = serializers.UserPrefSerializer(user_pref,
                                                    data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ListUndecidedDog(APIView):
    # def get(self, request, format=None):
        # user = self.request.user
        # user_pref = models.UserPref.objects.get(user=user)
        #  preferred_dogs = Dog.objects.filter(
        #                       gender__in=user_pref.gender,
        #                       size__in=user_pref.size)
        # dogs = models.Dog.objects.filter(
            
    
    
