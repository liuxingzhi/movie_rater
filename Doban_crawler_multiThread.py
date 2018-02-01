import requests
import pandas as pd
from sqlalchemy import create_engine
from queue import Queue
# from threading import Thread
import _thread

id_csv = "movie_ids.csv"


def crawl_poster(id, url):
    pic = requests.get(url).content
    file_name = 'static/poster/{id}.jpg'.format(id=id)
    f = open(file_name, "wb")
    f.write(pic)
    f.close()


def crawl_ids(write_to):
    doban = 'http://api.douban.com/v2/movie/top250?start=%d&count=50'
    movie_ids = set()
    for index in range(0, 250, 50):
        response = requests.get(doban % index)
        data = response.json()
        # print(type(data))
        movies = data['subjects']
        for movie in movies:
            # print(movie['id'], movie['title'])
            # print(movie)
            movie_ids.add(movie['id'])
        print("I am crawling", len(movie_ids))
    # print(movie_ids)
    # print(len(movie_ids))
    id_list = list(movie_ids)
    id_series = pd.Series(id_list)
    id_series.to_csv(write_to)


# crawl_ids(id_csv)

count = 0


# help method
def add_info(que, info, lock):
    global count
    while not que.empty():
        id = que.get()
        # print("running!", id)
        r = requests.get('http://api.douban.com/v2/movie/subject/%s' % id)
        if r.status_code != 200:
            count += 1
            print("failed", count)
            continue
        movie = r.json()
        # print(id)
        info.put({
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
        # print(movie['title'], movie['id'])
    lock.release()


def crawl_info_from_ids(read_from):
    info = Queue()
    que = Queue()
    for id in pd.Series.from_csv(read_from).tolist():
        que.put(id)
        # print(id)
    print("there are ids in total", que.qsize())
    # for id in movie_ids:
    #     add_info(id)
    locks = []
    for i in range(10):
        lock = _thread.allocate_lock()
        lock.acquire()
        locks.append(lock)
    for index, lock in enumerate(locks):
        try:
            _thread.start_new_thread(add_info, (que, info, lock))
            print("started a new thread", index)
        except:
            print("Error: unable to start thread")

    for lock in locks:
        while lock.locked():
            pass

    li = []
    for i in range(info.qsize()):
        li.append(info.get())
    df = pd.DataFrame(li)
    engine = create_engine('sqlite:///MovieSite.db')
    df.to_sql('movie', engine, if_exists='replace')
    print("this is dataframe", df)


def main():
    # crawl_ids(id_csv)
    crawl_info_from_ids(id_csv)


if __name__ == '__main__':
    main()
