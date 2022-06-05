from rest_framework import serializers

from company.models import Company, CompanyProfile


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'company_ticker']


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['ESG_score', 'environment', 'social', 'governance', 'rank', 'total_industries', 'company']
