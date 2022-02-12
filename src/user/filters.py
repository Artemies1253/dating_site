from django_filters import rest_framework as filters
from src.user.models import User


class UserListFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "gender": ("iexact",),
        }
