import torndb
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options


define("port", default=8080, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="poll database host")
define("mysql_database", default="polldb", help="poll database name")
define("mysql_user", default="root", help="poll database user")
define("mysql_password", default="01030605aldqaiqian65",
       help="poll database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/poll", IndexHandler),
            (r"/poll/([0-9]+)", DetailHandler),
            (r"/poll/([0-9]+)/results", ResultsHandler),
            (r"/poll/([0-9]+)/votes", VotesHandler),
            (r"/poll/([0-9]+)/addschoice", AddsChoiceHandler),
            (r"/poll/adds", AddsHandler),
        ]
        super(Application, self).__init__(handlers, template_path="templates")

        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db


class IndexHandler(BaseHandler):
    def get(self):
        latest_poll_list = self.db.query(
            "SELECT * FROM polls_poll ORDER BY pub_date DESC LIMIT 5")
        self.render("index.html", latest_poll_list=latest_poll_list)


class DetailHandler(BaseHandler):
    def get(self, poll_id):
        poll = self.db.query(
            "SELECT * FROM polls_poll WHERE id=%d" % int(poll_id))
        if not poll:
            raise tornado.web.HTTPError(404)
        choices = self.db.query(
            "SELECT * FROM polls_choice WHERE poll_id=%d" % int(poll_id))

        self.render("detail.html", poll=poll[0], choices=choices)


class ResultsHandler(BaseHandler):
    def get(self, poll_id):
        poll = self.db.query(
            "SELECT * FROM polls_poll WHERE id=%d" % int(poll_id))
        if not poll:
            raise tornado.web.HTTPError(404)
        choice = self.db.query(
            "SELECT * FROM polls_choice WHERE poll_id=%d" % int(poll_id))
        if not choice:
            raise tornado.web.HTTPError(404)
        else:
            self.render("results.html", poll=poll[0], choices=choice)


class VotesHandler(BaseHandler):
    def post(self, poll_id):
        poll = self.db.query("SELECT * FROM polls_poll WHERE id=%d" % int(poll_id))
        if not poll:
            raise tornado.web.HTTPError(404)
        else:
            selected_choice = self.get_argument("vote")
            if not selected_choice:
                self.redirect("/poll")
            else:
                self.db.execute(
                    "UPDATE polls_choice SET votes = votes + 1 WHERE id='%s'" %
                    (selected_choice,))
                self.redirect("/poll/%s/results" % poll_id)


class AddsChoiceHandler(BaseHandler):
    def post(self, poll_id):
        choice = self.get_argument("choice", default=None)

        self.db.execute(
            "INSERT INTO polls_choice(choice, poll_id) VALUES('%s', %d)" % (choice, int(poll_id)))

        #self.redirect("localhost:8000/poll" + poll_id, permanent=True, status=None)
        self.redirect("/poll/%s" % poll_id)


class AddsHandler(BaseHandler):
    def post(self):

        question = self.get_argument("question", default=None)

        self.db.execute(
            "INSERT INTO polls_poll(question, pub_date) VALUES('%s', NOW())" % (question,)
        )

        self.redirect("/poll")


def main():
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
import torndb
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options


define("port", default=8080, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="poll database host")
define("mysql_database", default="polldb", help="poll database name")
define("mysql_user", default="root", help="poll database user")
define("mysql_password", default="01030605aldqaiqian65",
       help="poll database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/poll", IndexHandler),
            (r"/poll/([0-9]+)", DetailHandler),
            (r"/poll/([0-9]+)/results", ResultsHandler),
            (r"/poll/([0-9]+)/votes", VotesHandler),
            (r"/poll/([0-9]+)/addschoice", AddsChoiceHandler),
            (r"/poll/adds", AddsHandler),
        ]
        super(Application, self).__init__(handlers, template_path="templates")

        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db


class IndexHandler(BaseHandler):
    def get(self):
        latest_poll_list = self.db.query(
            "SELECT * FROM polls_poll ORDER BY pub_date DESC LIMIT 5")
        self.render("index.html", latest_poll_list=latest_poll_list)


class DetailHandler(BaseHandler):
    def get(self, poll_id):
        poll = self.db.query(
            "SELECT * FROM polls_poll WHERE id=%d" % int(poll_id))
        if not poll:
            raise tornado.web.HTTPError(404)
        choices = self.db.query(
            "SELECT * FROM polls_choice WHERE poll_id=%d" % int(poll_id))

        self.render("detail.html", poll=poll[0], choices=choices)


class ResultsHandler(BaseHandler):
    def get(self, poll_id):
        poll = self.db.query(
            "SELECT * FROM polls_poll WHERE id=%d" % int(poll_id))
        if not poll:
            raise tornado.web.HTTPError(404)
        choice = self.db.query(
            "SELECT * FROM polls_choice WHERE poll_id=%d" % int(poll_id))
        if not choice:
            raise tornado.web.HTTPError(404)
        else:
            self.render("results.html", poll=poll[0], choices=choice)


class VotesHandler(BaseHandler):
    def post(self, poll_id):
        poll = self.db.query("SELECT * FROM polls_poll WHERE id=%d" % int(poll_id))
        if not poll:
            raise tornado.web.HTTPError(404)
        else:
            selected_choice = self.get_argument("vote")
            if not selected_choice:
                self.redirect("/poll")
            else:
                self.db.execute(
                    "UPDATE polls_choice SET votes = votes + 1 WHERE id='%s'" %
                    (selected_choice,))
                self.redirect("/poll/%s/results" % poll_id)


class AddsChoiceHandler(BaseHandler):
    def post(self, poll_id):
        choice = self.get_argument("choice", default=None)

        self.db.execute(
            "INSERT INTO polls_choice(choice, poll_id) VALUES('%s', %d)" % (choice, int(poll_id)))

        #self.redirect("localhost:8000/poll" + poll_id, permanent=True, status=None)
        self.redirect("/poll/%s" % poll_id)


class AddsHandler(BaseHandler):
    def post(self):

        question = self.get_argument("question", default=None)

        self.db.execute(
            "INSERT INTO polls_poll(question, pub_date) VALUES('%s', NOW())" % (question,)
        )

        self.redirect("/poll")


def main():
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

