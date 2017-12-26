import requests
import pandas as pd
from sqlalchemy import create_engine

movie_ids = set()

for index in range(0, 50, 50):
    response = requests.get('http://api.douban.com/v2/movie/top250?start=%d&count=50' % index)
    data = response.json()
    # print(type(data))
    movies = data['subjects']
    for movie in movies:
        # print(movie['id'], movie['title'])
        # print(movie)
        movie_ids.add(movie['id'])

print(movie_ids)

info = []
# find first 10
count = 0
for id in movie_ids:
    r = requests.get('http://api.douban.com/v2/movie/subject/%s' % id)
    if r.status_code != 200:
        continue
    movie = r.json()
    # print(id)
    info.append({
        "id" : int(movie['id']),
        "title" : movie['title'],
        "origin" : movie['original_title'],
        "url" : movie['alt'],
        "rating" : movie['rating']['average'],
        "image" : movie['images']['large'],
        "directors" : ','.join([d['name'] for d in movie['directors']]),
        "casts" : ','.join([c['name'] for c in movie['casts']]),
        "year" : movie['year'],
        "genres" : ','.join(movie['genres']),
        "countries" : ','.join(movie['countries']),
        "summary" : movie['summary'],
    })
    # print(movie['title'], movie['id'])
    count += 1
    if count > 10:
        break;
df = pd.DataFrame(info)

engine = create_engine('sqlite:///MovieSite.db')
df.to_sql('movie', engine, flavor='sqlite')
print(df)