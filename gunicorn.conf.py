import multiprocessing

bind = "0.0.0.0:9000"
#workers = 1
workers = multiprocessing.cpu_count() * 2 + 1
raw_env = ["DJANGO_SETTINGS_MODULE=AuroraIOT.settings.prod"]
accesslog = "./logs/gunicorn-access.log"
errorlog = "./logs/gunicorn-error.log"