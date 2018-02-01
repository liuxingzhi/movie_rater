import requests
import pandas as pd
from sqlalchemy import create_engine

id_csv = "movie_ids.csv"


def crawl_poster(id, url):
    pic = requests.get(url).content
    file_name = 'static/poster/{id}.jpg'.format(id=id)
    f = open(file_name, "wb")
    f.write(pic)
    f.close()


def crawl_ids(write_to):
    doban = 'http://api.douban.com/v2/movie/top250'  # 参数: ?start=%d&count=50'
    movie_ids = set()
    for index in range(0, 250, 50):
        params = {'start': index, 'count': 50}
        response = requests.get(doban, params=params)
        data = response.json()
        # print(type(data))
        movies = data['subjects']
        for movie in movies:
            # print(movie['id'], movie['title'])
            # print(movie)
            movie_ids.add(movie['id'])
    print(movie_ids)
    print("ids in total", len(movie_ids))
    id_list = list(movie_ids)
    id_series = pd.Series(id_list)
    id_series.to_csv(write_to)


# help method
def add_info(movie_ids, info):
    for id in movie_ids:
        r = requests.get('http://api.douban.com/v2/movie/subject/%s' % id)
        if r.status_code != 200:
            continue
        movie = r.json()
        # print(id)
        info.append({
            "id": int(movie['id']),
            "title": movie['title'],
            "origin": movie['original_title'],
            "url": movie['alt'],
            "rating": movie['rating']['average'],
            "image": movie['images']['large'],
            "directors": ','.join([d['name'] for d in movie['directors']]),
            "casts": ','.join([c['name'] for c in movie['casts']]),
            "year": movie['year'],
            "genres": ','.join(movie['genres']),
            "countries": ','.join(movie['countries']),
            "summary": movie['summary'],
        })
        crawl_poster(movie['id'], movie['images']['large'])
        print(movie['title'], movie['id'])


def crawl_info_from_ids(read_from):
    info = []
    movie_ids = pd.Series.from_csv(read_from).tolist()
    add_info(movie_ids, info)
    df = pd.DataFrame(info)
    engine = create_engine('sqlite:///MovieSite.db')
    df.to_sql('movie', engine, if_exists='replace')
    print("this is dataframe", df)


def main():
    crawl_ids(id_csv)
    # crawl_info_from_ids(id_csv)


if __name__ == '__main__':
    main()
