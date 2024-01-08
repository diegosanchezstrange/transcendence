# transcendence
Soon you will know that you’ve already known things that you thought you didn’t know

## Install dependencies
### Ubuntu
```
sudo apt install python3-virtualenv
```
```
virtualenv -p /usr/bin/python3 transcendence
```
```
source transcendence/bin/activate
```
```
sudo apt install -Y python3-pip
```

### MacOS

Homebrew
```
curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C ~/.brew
```
Python
```
brew install python
```

## Usage
```
cd srcs
docker-compose --env-file .env.dockerized up --build
```
