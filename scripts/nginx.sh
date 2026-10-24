
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/project_devops/nginx/nginx.conf /etc/nginx/sites-available/config
sudo ln -s /etc/nginx/sites-available/config /etc/nginx/sites-enabled/config
#sudo ln -s /etc/nginx/sites-available/config /etc/nginx/sites-enabled/default
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx

