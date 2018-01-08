from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

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
    

    
