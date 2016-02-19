# mayan

###WARNING:
This is my own fork, and I have made modifications, if you wish to try mayan-edms, please download it from it's original source. What is written below is for my own use, and may not work in your case. My way of installing mayan-edms is most likely the improper way, but it has worked for my own specific environment.

INSTALLING MAYAN:

Enter tmux session:
tmux or tmux attach
(This allows you to exit the terminal without killing the mayan-edms process).

Enter root:
sudo -i
(If you do not run this, you will have to type 'sudo' before every command)

Install dependencies:
apt-get update && apt-get install -y netcat-openbsd python-dev python-pip gpgv nginx libpq-dev git-core libjpeg-dev libmagic1 libpng-dev libreoffice libtiff-dev gcc ghostscript gpgv tesseract-ocr unpaper poppler-utils && apt-get clean && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/archives/*.deb

Install mayan-edms:
pip install mayan-edms

CD into the python dist-packages folder:
cd /usr/local/lib/python2.7/dist-packages

Remove old mayan directory, if cloning from github:
rm -r mayan

Clone from github:
git clone [github repository address]

What I used:
git clone https://github.com/trillobite/mayan.git

CD into the directory where mayan-edms.py resides:
cd mayan/bin

SETTING UP MAYAN:
python mayan-edms.py initialsetup

Start it:
python mayan-edms.py runserver

Install nginx:
sudo apt-get install nginx

Setup the nginx config:
cd /etc/nginx
vim nginx.conf

user  root;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;

    server {
        listen    8080;
    }
}

cd /etc/nginx/conf.d
vim default.conf

server {
    listen       8080;
    #server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/log/host.access.log  main;

    location / {
        proxy_pass                              http://127.0.0.1:8000;
        proxy_set_header    Host                $host:8080;
        proxy_set_header    X-Real-IP           $remote_addr;
        proxy_set_header    X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header    Via                 "nginx";
    }
}

cd /etc/nginx/sites-available
vim default

server {
        listen 8080 default_server;
        listen [::]:8080 default_server;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }
}

restart nginx:
service nginx reload




Mayan virtual environment information, if using venv:
Virtual environment: /venv/local/lib/python2.7/site-packages/mayan
Static files: /venv/local/lib/python2.7/site-packages/mayan/apps/appearance
bootstrap: /mayan/apps/appearance/static/appearance/packages/bootstrap-3*
bootstrap css: /mayan/apps/appearance/static/appearance/packages/bootstrap-3*/css
js scripts in mayan_edms/contrib/scripts





MAYAN FILE STRUCTURE

IMAGES: /mayan/apps/appearance/static/appearance/images
favicon.ico		← The icon which shows at the very top of the screen in the browser.
Loading.png		← The rotating image to display when something is loading.

CSS: /mayan/apps/appearance/static/appearance
base.css			← defines fonts. Location: /appearance/static/appearance/css
bootstrap.css		← css for div elements on the DOM. /appearance/static/appearance/packages/boot*/css
bootstrap-theme.css	← Looks like a bootstrap generated standard theme css file. Same location as above.

HTML:  /appearance/templates
base.html			← Appears to be the main HTML file that everything else attaches to.





My project notes:
Use remote database
use s3 drive
I need to learn bootstrap and work on the theme

can find the directory where files are stored, by accessing the mayan-edms settings.

Logo is a font-awesome icon.

The HTML for the brand logo is located in base.html under the class name 'navbar-brand.' It is designed to be a link, and the css settings is located in bootstrap.css, and base.css. Right now, it is set as plain text with the bootstrap definition. I need to replace this with a simple image.

I need to figure out how this webpage manages it's images.

Change log:
Cloned mayan-edms into my trillobite github
Inserted the new logo, and made changes to the base.html to show the logo

-Need to change the name of my mayan-edms clone to “mayan,” so it can be directly deployed into the python folder


Note: 
If you add or change this documentation slightly, increment the documentation version number like this: 1.2 → 1.3

If you add or change this documentation drastically, increment the documentation version number like this: 1.2 → 2.0
