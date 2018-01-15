import web

# default port: http://127.0.0.1:8080/
db = web.database(dbn='sqlite', db='MovieSite.db')
render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/movie/(\d+)', 'movie',
)

class index:
    def GET(self):
        # page = ''
        # for m in movies:
        #     page += '%s (%d)\n' % (m['title'], m['year'])
        # return page
        movies = db.select('movie')
        return render.index(movies)

    def POST(self):
        data = web.input()
        # print(type(data))
        # print(type(data.title))
        # 用r''是为了防止 python 默认对于字符串中 % 的转义。
        condition = r'title like"%' + data.title + r'%"'
        # database syntax =
        # select * from movie where title like "%搜索内容%";
        movies = db.select('movie', where = condition)
        return render.index(movies)

class movie:
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


