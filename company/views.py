from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from company.models import Company, CompanyProfile
from company.serializers import CompanySerializer, CompanyProfileSerializer


class CompanyListAPIView(generics.ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class CompanyProfileRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanyProfileSerializer
    queryset = CompanyProfile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        company = Company.objects.filter(company_ticker=self.request.query_params.get('ricCode', None))
        company_profile = CompanyProfile.objects.filter(company=company[0])
        return queryset.get(pk=company_profile[0].id)
