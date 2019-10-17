import ConfigParser
import logging

from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, session, redirect, request, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route('/')
def index():
    this_route = url_for('.index')
    app.logger.info("Logging a test message from" + this_route)
    return render_template('index.html'), 404

@app.route('/login/')
@app.route('/login/<message>')
def login(message=None):
    if (message != None):
        flash(message)
    else:
        flash(u'A default message')
    return redirect(url_for('index'))

@app.route('/config/')
def config():
    str1 = []
    str1.append('Debug: '+str(app.config['DEBUG']))
    str1.append('port: '+app.config['port'])
    str1.append('url: '+app.config['url'])
    str1.append('ip_address: '+app.config['ip_address'])
    return '\t'.join(str1)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/users/')
def users():
    names = ['simon', 'thomas', 'lee', 'jamie', 'sylvester', 'viktor']
    return render_template('loops.html', names=names)

@app.route('/inherits/')
def inherits():
    return render_template('base.html')

@app.route('/inherits/one/')
def inherits_one():
    return render_template('inherits1.html')

@app.route('/inherits/two/')
def inherits_two():
    return render_template('inherits2.html')

@app.route('/session/write/<name>/')
def write(name=None):
    session['name'] = name
    return "Wrote %s into 'name' key of session" % name

@app.route('/session/read/')
def read():
    try:
        if(session['name']):
            return str(session['name'])
    except KeyError:
        pass
    return "No session variable set for 'name' key"

@app.route('/session/remove/')
def remove():
    session.pop('name', None)
    return "Removed key 'name' from session"

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")

        app.config['log_file'] = config.get("logging", "name")
        app.config['log_location'] = config.get("logging", "location")
        app.config['log_level'] = config.get("logging", "level")
    except:
        print "Could not read configs from: ", config_location

def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024*1024*10, backupCount=1024)
    file_handler.setLevel( app.config['log_level'] )
    formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.setLevel( app.config['log_level'] )
    app.logger.addHandler(file_handler)

if __name__ == "__main__":
    init(app)
    logs(app)
    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port']))
