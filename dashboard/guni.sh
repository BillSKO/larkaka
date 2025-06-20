#!/bin/bash
echo "🔄 Stoppar Gunicorn..."
sudo systemctl stop nikola-gunicorn.service
sleep 1
echo "🔄 Startar Gunicorn..."
sudo systemctl daemon-reload
sudo systemctl start nikola-gunicorn.service
sleep 2
echo "📋 Status Gunicorn:"
sudo systemctl status nikola-gunicorn.service -n 15 --no-pager
