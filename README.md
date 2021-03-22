# README
>Para configuración del aplicativo de prueba de generacion de Constancias y Recibos de pago, version 0.1 Marzo del 2021. Maintained by <a rel="" href="https://github.com/davidcorrea743">David Correa</a> and <a rel="" href="https://github.com/josean7link">Josean Martinez</a>.

### Instalacion de Paquetes en Linux.
Instalamos los paquetes necesarios para tener Development Mariadb Server y Cliente Nginx Python3/pip PHP/phpmyadmin.

``sudo aptitude install default-libmysqlclient-dev build-essential libldap2-dev mariadb-server-10.3 mariadb-client-10.3 nginx phpmyadmin python3-dev python3-pip``

``sudo aptitude install php7.2 php7.2-bz2 php7.2-curl php7.2-cli php7.2-gd php7.2-json php7.2-mysql php7.2-mbstring php7.2-readline php7.2-opcache php7.2-xml php7.2-zip``

``sudo aptitude install php7.4 php7.4-bz2 php7.4-curl php7.4-cli php7.4-gd php7.4-json php7.4-mysql php7.4-mbstring php7.4-readline php7.4-opcache php7.4-xml php7.4-zip``

### Administar la Database con phpmyadmin.
Creamos el enlace virtual al directorio de servidores web para phpmyadmin con el nombre de database.

``cd /var/www/html
sudo ln -s /usr/share/phpmyadmin database``

### Mariadb como Database.
Abrimos el servidor Mariadb para crear las bases de datos y los usuarios necesarios.

``sudo mariadb -u root -p``

``CREATE DATABASE tramites;
DROP USER 'senifa'@'localhost';
DROP USER 'phpmyadmin'@'localhost';
FLUSH PRIVILEGES;``

``CREATE USER 'phpmyadmin'@'localhost' IDENTIFIED BY 'Bane123*';
CREATE USER 'senifa'@'localhost' IDENTIFIED BY '*.Inf2021.*';
GRANT ALL PRIVILEGES ON *.* TO 'phpmyadmin'@'localhost';
GRANT ALL PRIVILEGES ON tramites.* TO 'senifa'@'localhost';
FLUSH PRIVILEGES;
exit``

### Configuración del Proyecto Django.
Asumiendo el proyecto esta en la carpeta $HOME con nombre django_project copiamos el proyecto a la carpeta /opt con el nombre Tramites.

``sudo rsync -ah ~/django_project /opt/Tramites
cd /opt/Tramites``

Cambiamos los permisos a la carpeta Tramites.

``sudo chown -Rf 1000:1000 /opt/Tramites``

Instalamos y creamos el entorno virtual con virtualenv.

``python3.8 -m pip install virtualenv
python3.8 -m virtualenv venv``

``python3.6 -m pip install virtualenv
python3.6 -m virtualenv venv``

Activamos el entorno virtual e instalamos los paquetes necesarios.

``source venv/bin/activate
venv/bin/python3.8 -m pip install django django-crispy-forms pillow mysqlclient gunicorn xhtml2pdf --no-color``

``venv/bin/python3.6 -m pip install django django-crispy-forms pillow mysqlclient gunicorn xhtml2pdf --no-color``

Realizamos las migraciones en la base de datos y creamos el superusuario Senifa.

``./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser --username Senifa --email '' --no-color``

### Configuraciones del servidor Nginx y Gunicorn.
Actualizamos el nombre del servidor.

``sudo nano etc/hosts``

``127.0.0.1  localhost   senifa.web``

Creamos los Enlaces Virtuales necesarios.

``cd /etc/nginx/sites-available/
sudo ln -s /opt/Tramites/etc/nginx/sites-available/tramites``

``cd ../sites-enabled/
sudo ln -s ../sites-available/tramites``

``cd /etc/systemd/system
sudo ln -s /opt/Tramites/etc/systemd/system/gunicorn.service
sudo ln -s /opt/Tramites/etc/systemd/system/gunicorn.socket``

Cambiamos el usuario de la carpeta Tramites del $USER a usuario de nginx www-data.

``sudo chown -Rf www-data:www-data /opt/Tramites``

Verificamos configuracion de Nginx y recargamos cambios al sistema, verificando si existe algun error.

``sudo nginx -t
sudo systemctl stop gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn.socket
sudo systemctl restart nginx.service
sudo systemctl status nginx.service
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn.service``

### Comprobación del aplicativo.

``http://senifa.web:8002/Tramites``
