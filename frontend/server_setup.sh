sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install mysql-client mysql-server
sudo a2enmod wsgi   
sudo apt-get install apache2-dev
sudo apt-get install git
sudo apt-get install gcc
sudo apt-get install g++
sudo apt-get install python-dev
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
pyenv install miniconda3-latest
vi .bashrc
source .bashrc
git clone https://github.com/aktivkohle/youtube-curation.git
cd youtube-curation/
pip install -r requirements.txt
python -m spacy download en
# also need to install the stopwords from nltk in python
pip install mod_wsgi
cd frontend
chmod 555 flaskapp.wsgi
chmod 555 similar_vids_frontend.py 
sudo chown -R ubuntu:www-data frontend
sudo chmod -R g+s frontend
sudo ln -sT ~/youtube-curation/frontend /var/www/html/frontend
mysql -u root -p
# now run "source backupfile.dump" after bringing the backupfile here with scp

# edit the apache file, restart and check the error log if necessary
sudo vi /etc/apache2/sites-enabled/000-default.conf
sudo apachectl restart
cat /var/log/apache2/error.log

 



