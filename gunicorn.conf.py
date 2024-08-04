import multiprocessing

bind = "0.0.0.0:9000"
#workers = 1
workers = multiprocessing.cpu_count() * 2 + 1
raw_env = ["DJANGO_SETTINGS_MODULE=AuroraIOT.settings.prod"]
# Access log - records incoming HTTP requests
accesslog = "./logs/gunicorn-access.log"
# Error log - records Gunicorn server goings-on
errorlog = "./logs/gunicorn-error.log"
# How verbose the Gunicorn error logs should be 
loglevel = "info"