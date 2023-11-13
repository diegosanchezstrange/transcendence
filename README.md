# transcendence
Soon you will know that you’ve already known things that you thought you didn’t know

## Local setup (provisional)
### Ubuntu
##### Virtualenv
- sudo apt install python3-virtualenv
- virtualenv -p /usr/bin/python3 transcendence
- source transcendence/bin/activate

##### Django
- sudo apt install -Y python3-pip
- pip3 install Django
- python manage.py migrate
- python manage.py runserver

##### Gettext
- /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
- (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> ~/.bashrc
- eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
- brew install gettext
