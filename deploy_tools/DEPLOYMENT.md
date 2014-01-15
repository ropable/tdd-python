Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip-3.3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com
* copy conf file into /etc/init
* sudo service start <name of copied file>

## Folder structure:
Assume we have a user account at /var/www

/var/www
└── domain_name
     ├── database
     ├── source
     ├── static
     └── virtualenv
