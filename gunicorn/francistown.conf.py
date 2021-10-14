# esr21 gunicorn.conf
import os

SOURCE_ROOT = os.path.expanduser('~/source')

errorlog = os.path.join(
    SOURCE_ROOT, 'esr21/logs/esr21-francistown-gunicorn-error.log')
accesslog = os.path.join(
    SOURCE_ROOT, 'esr21/logs/esr21-francistown-gunicorn-access.log')
loglevel = 'debug'
pidfile = os.path.join(SOURCE_ROOT, 'esr21/logs/esr21-francistown.pid')

workers = 2  # the number of recommended workers is '2 * number of CPUs + 1'

raw_env = ['DJANGO_SETTINGS_MODULE=esr21.community.francistown']

bind = "127.0.0.1:9013"
