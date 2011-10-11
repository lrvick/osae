import os
import sqlite3
import hashlib
from flask import g, Flask, request, session, render_template
from gevent.pywsgi import WSGIServer
from ConfigParser import ConfigParser

config = ConfigParser()

config.read('config.ini')

host = config.get('DEFAULT','host')
port = config.getint('DEFAULT','port')
verbose = config.getboolean('DEFAULT','verbose')
debug = config.getboolean('DEFAULT','debug')

DATABASE="%s/samples.db" % os.getcwd()

app = Flask(__name__)

def connect_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE item (id integer primary key, user_hash text, text text unique, sentiment text)''')
    else:
        conn = sqlite3.connect(DATABASE)
    return conn

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/', methods=['POST','GET'])
def index():
    """ Returns main interface """
    if request.method == 'POST':
        sample = request.form['sample']
        sentiment = request.form['submit']
        user_hash = hashlib.sha1('//'.join([str(request.user_agent), request.remote_addr])).hexdigest()
        if sentiment != 'neutral':
            try:
                g.db.execute('INSERT INTO item VALUES (NULL,?,?,?)',[user_hash,sample,sentiment])
                g.db.commit()
            except Exception, e:
                print e
    return render_template('base.html',counter=session.get('counter',0))

if __name__ == '__main__':
    if verbose:
        print "Starting osae on %s:%s" % (host,port)
    app.debug = debug
    http_server = WSGIServer((host,port), app)
    http_server.serve_forever()
