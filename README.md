# transcendence
Soon you will know that you’ve already known things that you thought you didn’t know

## Local setup (provisional)
### Ubuntu
- sudo apt install python3-virtualenv
- virtualenv -p /usr/bin/python3 transcendence
- source transcendence/bin/activate
- sudo apt install -Y python3-pip
- pip3 install Django
- python manage.py migrate
- python manage.py runserver
