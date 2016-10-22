import requests
import pickle
import collections
import itertools

#newssapi_url = 'https://newsapi.org/v1/sources?language=en&country=gb&category=business'
#newssapi_url = 'https://newsapi.org/v1/articles?'
#nytimes_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
#mbrain_testing_url = 'http://api.m-brain.com/mapi-lab/v1.1/search/search.json?api_key=tietoelo_hktn_team_3_evev6jfb39qp22s9llkqr55qrg_1475839164&query=entrepreneur AND ( trend OR vision OR hype )&category=editorial%2Cblog%2Cchat%2Cfacebook%2Ctwitter%2Cinstagram&lang=en&publishDateSince=2016-06-07T00%3A00%3A00.000Z&from=1&max=50&rank=relevance&noDups=true&showSentiment=true&showSnippet=true&showTotal=true'
#newsapi_params = {'source': 'cnn', 'apiKey': 'aba3c9480d084df9adef4e0aafb21bb4', 'articles': {'publishedAt': '2016-10-18'}}
#nytimes_params = {'begin_date': '20160101', 'end_date': '20160201'}

mbrain_url = 'http://api.m-brain.com/mapi-lab/v1.1/search/search.json?'
mbrain_params = {'api_key': 'tietoelo_hktn_team_3_evev6jfb39qp22s9llkqr55qrg_1475839164',
                 'query': 'entrepreneur OR entrepreneurship OR startups OR business OR retail OR strategy'
                          'OR management OR company OR leadership',
                 'defaultOperator': 'OR',
                 'category': 'editorial',
                 'lang': 'en',
                 'publishDateSince': '2016-01-01',
                 'publishDateUntil': '2016-10-10',
                 'region': 'us',
                 'from': 1,
                 'max': 1000,
                 'showTotal': 'true',
                 'noDups': 'true',
                 'orIndustryTopic': 'best:Technology & Communications'
                 }
region_eu = ['se', 'fi', 'fr', 'de', 'it', 'es', 'ch', 'gb']
region_eu = ['gb']
region_us = ['us']

years = [2016]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
days = [1, 11, 21]

categories = dict()
categories['technology'] = ['best:Technology & Communications', 'best:Science & Research',
                          'best:Energy', ]
categories['politics'] = ['best:Politics & Society']
categories['economy'] = ['best:Business & Finance', 'best:Construction & Habitation']
categories['lifestyles'] = ['best:Environment & Nature', 'best:Food & Beverage', 'best:Travelling & Vehicles',
                          'best:Entertainment & Hobbies', 'best:Health & Well-being']

def retrieve_from_mbrain(regions, output_name):
    output_list = []
    for region in regions:
        for (year, month, day) in itertools.product(*[years, months, days]):
            start_date = '%d-%02d-%02d' % (year, month, day)
            end_date = '%d-%02d-%02d' % (year, month, day + 10)
            print('%s - %s' % (start_date, end_date))

            for cat, subcats in categories.items():
                for subcat in subcats:
                    mbrain_params['publishDateSince'] = start_date
                    mbrain_params['publishDateUntil'] = end_date
                    mbrain_params['orIndustryTopic'] = subcat
                    mbrain_params['region'] = region
                    response = requests.get(mbrain_url, params=mbrain_params)
                    response = response.json()
                    response = response['docs']

                    for doc in response:
                        # omit the headlines that are too short!
                        if len(doc['title'].split()) <= 4:
                            continue
                        output_json = collections.OrderedDict()
                        output_json['my_category'] = cat
                        output_json['industryTopics'] = subcat.replace('best:', '')
                        output_json['publishDate'] = doc['publishDate']
                        output_json['title'] = doc['title']
                        output_json['url'] = doc['url']
                        output_list.append(output_json)

    with open(output_name, 'wb') as fp:
        pickle.dump(output_list, fp)

    return output_list

output_list_eu = retrieve_from_mbrain(region_eu, 'train_eu.pickle')
output_list_us = retrieve_from_mbrain(region_us, 'train_us.pickle')