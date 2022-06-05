# django-crawler-ESGscore

first create a local-settings.py in scorebot that contains your postgresql database configs:

DB = { 'NAME': 'database name', 'USER': 'database user name', 'PASSWORD': 'database pass', 'HOST': 'database ip', 'PORT': 'database port', }


then you must run manualy the crawler.py to update database(we could do it with a api or time schedule too). it will get the first 101 companies data and scores(not all cause of low ping and resources) and save in database.

API's:

  get() method to "site/api/register/" to get the token for register
  
  get() method to "site/api/companieslist/" to get list of companies that we have theyr scores
  
  get() method to "site/api/companyscore/?ricCode=company_ric_code" to get scores of company_ric_code
