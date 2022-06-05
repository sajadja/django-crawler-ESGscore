from django.db import models
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    name = models.CharField(_('name'), max_length=500, unique=True)
    company_ticker = models.CharField(_('company ticker'), max_length=200, unique=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class CompanyProfile(models.Model):
    ESG_score = models.PositiveSmallIntegerField(_('ESG score'))
    environment = models.PositiveSmallIntegerField(_('environment'))
    social = models.PositiveSmallIntegerField(_('social'))
    governance = models.PositiveSmallIntegerField(_('governance'))
    rank = models.PositiveSmallIntegerField(_('rank'))
    total_industries = models.PositiveSmallIntegerField(_('total industries'))
    company = models.OneToOneField(Company, related_name='company_profile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'company profile'
        verbose_name_plural = 'companies profile'
