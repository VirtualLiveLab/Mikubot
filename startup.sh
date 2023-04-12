#!/bin/sh
echo "start startup.sh"

echo "
[supervisord]
nodaemon=true
[program:python1]
command=python /app/main.py 
stdout_logfile=/app/stderr_logfile.log
stdout_logfile_maxbytes=0
stderr_logfile=/app/stdout_logfile.log
stderr_logfile_maxbytes=0
autostart=true
autorestart=true
">/etc/supervisor/conf.d/supervisord.conf

/usr/bin/supervisord
