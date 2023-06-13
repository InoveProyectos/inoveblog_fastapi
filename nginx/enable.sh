ln -sf $(dirname -- "$(realpath -- $0;)";)/inoveblog /etc/nginx/sites-enabled/inoveblog
sudo systemctl restart nginx.service