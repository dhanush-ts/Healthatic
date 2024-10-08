from django.urls import path
from skinserver.api.views import UserListAV, Login, HospitalListAV, HospitalDetailAV

urlpatterns = [
    path('signup/', UserListAV.as_view(), name='user-list'),
    path('login/', Login.as_view(), name='user-detail'),
    path('hospitals/', HospitalListAV.as_view(), name='hospital-list'),
    path('hospitals/<int:pk>/', HospitalDetailAV.as_view(), name='hospital-detail'),
]