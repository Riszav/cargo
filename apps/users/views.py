from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsAdmin
from . import models, serializers


class CountryListAPIView(ListAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class UserListAPIView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdmin]


class UserCreateAPIView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer


class UserDetailAPIView(RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
    

class UserClientDetailAPIView(RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserClientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return models.User.objects.get(client_id=self.request.user.id)
    
