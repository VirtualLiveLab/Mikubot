#!/bin/sh
echo "start startup.sh"

echo "
[supervisord]
nodaemon=true
[program:python1]
command=python /app/main.py 
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
autostart=true
autorestart=true
[program:python2]
command=python /app/button.py 
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
autostart=true
autorestart=true
">/etc/supervisor/conf.d/supervisord.conf

/usr/bin/supervisord