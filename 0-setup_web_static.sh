#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static
sudo apt-get -y update
# Check if Nginx is installed, if not proceed to install
sudo apt-get -y install nginx
sudo ufw allow 'nginx HTTP'
sudo service nginx start
# Create directories if they dont exist, -p ensures
# parent dirs are created as well
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
# Fake HTML file created
samba="
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo "$samba" | sudo tee /data/web_static/releases/test/index.html
# Remove symbolic link if exists (-f) before creating a new one
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Configure Nginx to serve alias content
if ! sudo grep -q "alias /data/web_static/current/;" /etc/nginx/sites-enabled/default; then
    sudo sed -i "\#server_name _;#a \\
        location /hbnb_static { \\
            alias /data/web_static/current/; \\
        } \\
        "  /etc/nginx/sites-enabled/default
fi
sudo chown -R ubuntu:ubuntu /data/
sudo service nginx reload
