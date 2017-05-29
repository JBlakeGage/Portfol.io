[uwsgi]
socket = /tmp/uwsgi.sock
http = 0.0.0.0:5000
harakiri = 60
module = run
callable = topics_app
master = true
uid = 1
gid = 1
die-on-term = true
processes = 4
threads = 2
{% if DEBUG %}python-autoreload = 1{% endif %}
