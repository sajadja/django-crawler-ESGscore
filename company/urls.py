from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

from company.views import CompanyListAPIView, CompanyProfileRetrieveAPIView

urlpatterns = [
    path('register/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('companieslist/', CompanyListAPIView.as_view(), name='companies_list'),
    path('companyscore/', CompanyProfileRetrieveAPIView.as_view(), name='companies_list')
]
