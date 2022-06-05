from django.contrib import admin
from django.contrib.admin import register

from company.models import Company, CompanyProfile


@register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_ticker']


@register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['ESG_score', 'environment', 'social', 'governance', 'rank', 'total_industries', 'company']
