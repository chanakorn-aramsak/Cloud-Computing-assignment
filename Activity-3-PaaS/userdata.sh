#!/bin/bash


# Install PHP
sudo yum install php-mysql php php-xml php-mcrypt php-mbstring php-cli mysql httpd tcpdump emacs -y

sudo yum update -y
# Start and Enable Apache:
sudo systemctl start httpd
sudo systemctl enable httpd


# usermod -a -G apache ec2-user
# chown -R ec2-user:apache /var/www
# chmod 2775 /var/www
# find /var/www -type d -exec chmod 2775 {} \;
# find /var/www -type f -exec chmod 0664 {} \;
cd /var/www/html
sudo wget https://raw.githubusercontent.com/chanakorn-aramsak/php-server/main/index.php
sudo wget https://raw.githubusercontent.com/chanakorn-aramsak/php-server/main/logo_aws_reduced.gif
sudo wget https://raw.githubusercontent.com/chanakorn-aramsak/php-server/main/styles.css