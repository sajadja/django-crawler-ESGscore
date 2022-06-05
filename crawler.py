from itertools import islice
import threading
import requests
import os
import django
import concurrent.futures
from queue import Queue
import logging


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scorebot.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "scorebot.settings"
django.setup()

from company.models import Company, CompanyProfile


def company_fill():
    logging.info('getting list of first 100 companies...')
    data_json = requests.get('https://www.refinitiv.com/bin/esg/esgsearchsuggestions')
    data = data_json.json()
    data = data[:101]
    if data_json.status_code == 200:
        batch_size = len(data)
        objs = (Company(name=each['companyName'], company_ticker=each['ricCode']) for each in data)
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Company.objects.bulk_create(batch, batch_size, ignore_conflicts=True)
    else:
        raise 'api not reachable'


def company_profile_fill():
    logging.info('getting profile and score of each company...')
    companies = Company.objects.all()

    def get_company_data(q):
        while True:
            try:
                company = q.get(timeout=6)
            except q.empty:
                return

            url = 'https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode=' + company.company_ticker
            company_data_json = requests.get(url)
            company_data = company_data_json.json()
            CompanyProfile.objects.update_or_create(
                ESG_score=company_data['esgScore']['TR.TRESG']['score'],
                environment=company_data['esgScore']['TR.EnvironmentPillar']['score'],
                social=company_data['esgScore']['TR.SocialPillar']['score'],
                governance=company_data['esgScore']['TR.GovernancePillar']['score'],
                rank=company_data['industryComparison']['rank'],
                total_industries=company_data['industryComparison']['totalIndustries'],
                company=company, defaults={'company': company})
            q.task_done()

    queue = Queue()
    for c in companies:
        queue.put_nowait(c)

    threads = list()
    for _ in range(5):
        x = threading.Thread(target=get_company_data, args=(queue,))
        threads.append(x)
        x.start()

    queue.join()
    for t in threads:
        t.join()

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(get_company_data, companies)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    company_fill()
    logging.info('list of companies saved.')
    company_profile_fill()
    logging.info('done!! database updated.')
