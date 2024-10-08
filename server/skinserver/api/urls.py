from django.urls import path
from skinserver.api.views import UserListAV, Login

urlpatterns = [
    path('signup/', UserListAV.as_view(), name='user-list'),
    path('login/', Login.as_view(), name='user-detail'),
]