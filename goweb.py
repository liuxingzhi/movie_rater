# -*- coding: utf-8 -*-
import web

# default port: http://127.0.0.1:8080/
db = web.database(dbn='sqlite', db='MovieSite.db')
render = web.template.render('templates/')

urls = (
    '/', 'Index',
    '/movie/(\d+)', 'Movie',
    '/cast/(.*)', 'Cast',
    '/director/(.*)', 'Director',
)


class Index:
    def GET(self):
        # page = ''
        # for m in movies:
        #     page += '%s (%d)\n' % (m['title'], m['year'])
        # return page
        # web.header('Content-Type', 'text/html;charset=UTF-8')
        movies = db.select('movie')
        count = db.query('select count(*) as count from movie')[0]['count']
        return render.index(movies, count, None)

    def POST(self):
        data = web.input()
        # print(type(data))
        # print(type(data.title))
        # 用r''是为了防止 python 默认对于字符串中 % 的转义。
        condition = r'title like"%' + data.title + r'%"'
        # database syntax
        # select * from movie where title like "%搜索内容%";
        movies = db.select('movie', where=condition)
        statement = 'select count(*) as count from movie where ' + condition
        result = db.query(statement)
        data = result[0]
        count = data['count']
        return render.index(movies, count, None)


class Movie:
    def GET(self, movie_id):
        movie_id = int(movie_id)
        movie = db.select('movie', where='id = $movie_id', vars=locals())[0]
        return render.movie(movie)

    # def GET(self, movie_id):
    #     movie = db.select('movie', where='id=$int(movie_id)', vars=locals())[0]
    #     return render.movie(movie)

    # def GET(self, movie_id):
    #     # movie_id = int(movie_id)
    #     # movie = db.select('movie', where='id=$movie_id', vars=locals())[0]
    #     condition = 'id=' + movie_id
    #     movie = db.select('movie', where=condition)[0]
    #     return render.movie(movie)


class Cast:
    def GET(self, cast_name):
        # cast_name is latin, I do not know why, but this work.
        name = cast_name.encode('ISO-8859-1').decode('utf-8')
        condition = r'casts like "%' + name + r'%"'
        movies = db.select('movie', where=condition)
        count = db.query('select count(*) as count from movie where ' + condition)[0]['count']
        return render.index(movies, count, name)


class Director:
    def GET(self, director_name):
        name = director_name.encode('ISO-8859-1').decode('utf-8')
        condition = r'directors like "%' + name + r'%"'
        movies = db.select('movie', where=condition)
        # be careful with white space, it's important or SQL syntax will go wrong
        count = db.query('select count(*) as count from movie where ' + condition)[0]['count']
        return render.index(movies, count, name)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

# movies = [
#     {'title': 'Forrest Gump',
#      'year': 1994,
#      },
#     {'title': 'Titanic',
#      'year': 1997,
#      },
# ]
