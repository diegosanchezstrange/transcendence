# transcendence
Soon you will know that you’ve already known things that you thought you didn’t know

## Local setup (provisional)
### Ubuntu
##### Virtualenv
 ```
 sudo apt install python3-virtualenv
 ```
```
virtualenv -p /usr/bin/python3 transcendence
```
```
source transcendence/bin/activate
```

##### Django
```
sudo apt install -Y python3-pip
```
```
pip3 install Django
```
```
python manage.py migrate
```
```
python manage.py runserver
```

##### PostgreSQL
```
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```
```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```
```
sudo apt-get update
```
```
sudo apt-get -y install postgresql
```
```
pip install psycopg2-binary
```

##### Gettext
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
```
(echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> ~/.bashrc
```
```
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```
```
brew install gettext
```
