from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from src.base.services import get_border_coordinates
from src.user.filters import UserListFilter
from src.user.models import User
from src.user.serializer import UserDetailSerializer


class UserList(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.object.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserListFilter
    permission_classes = (permissions.IsAuthenticated,)
    
    
class NearestUsers(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)
    #queryset = User.object.all()
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = UserListFilter    

    def get_queryset(self):
        user = self.request.user
        print(user.longitude)
        user = User.object.get(id=user.id)
        longitude = user.longitute
        latitude = user.latitude
        distance = 1
        border_coordinates = get_border_coordinates(longitude, latitude, distance)
        nearest_users_queryset = User.object.filter(longitude__lte=border_coordinates['max_longitude'])\
                                    .exclude(longitude__lt=border_coordinates['min_longitude'])\
                                    .exclude(latitude__gt=border_coordinates['max_latitude'])\
                                    .exclude(latitude__lt=border_coordinates['min_latitude'])\
                                    .exclude(id=user.id)
        return nearest_users_queryset

# class NearestUsers(viewsets.ViewSet):
#     #queryset = User.object.all()
    
#     def list(self, request):
#         longitude = request.user.longitude
#         latitude = request.user.latitude
#         nearest_users_queryset = User.object.filter(longitude__lte=longitude+0.016)\
#                                     .exclude(longitude__lt=longitude-0.16)\
#                                     .exclude(latitude__gt=latitude+0.009)\
#                                     .exclude(latitude__lt=latitude-0.009)\
#                                     .exclude(id=request.user.id)
#         serializer = UserDetailSerializer(nearest_users_queryset, many=True)
#         return Response(serializer.data)
    
    # def retrieve(self, request, pk=None):
    #     user = get_object_or_404(self.queryset, pk=pk)
    #     serializer = GameModelSerializer(user)
    #     return Response(serializer.data)
    
    
# class NearestUsers(APIView):
#     def get(self, request):
#         longitude = request.user.longitude
#         latitude = request.user.latitude
#         nearest_users = User.object.filter(longitude__lte=longitude+0.016)\
#                                     .exclude(longitude__lt=longitude-0.16)\
#                                     .exclude(latitude__gt=latitude+0.009)\
#                                     .exclude(latitude__lt=latitude-0.009)\
#                                     .exclude(id=request.user.id)
#         serialiser= UserDetailSerializer(nearest_users, many=True)
#         return Response(serialiser.data)