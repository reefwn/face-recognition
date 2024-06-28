# Face Recognition

## Running application
```
docker-compose up -d
```

## Running script

### Install pipenv

```
brew install pipenv
```

### Install dependencies

```
brew install cmake
pipenv --python 3.8 install
```

### Activate virtual environment
```
pipenv --python 3.8 shell
```

### Run script
```
# inside virtual environment

python identify_persons.py
python video.py
```

### Remove virtual environment
```
pipenv --rm
```

## Technologies & IDE

<div>
  <img style="float: left" src="https://raw.githubusercontent.com/jgthms/bulma/master/docs/images/bulma-banner.png" height="48" alt="bulma"> &nbsp;
  <img style="float: left" src="https://flask-wtf.readthedocs.io/en/1.2.x/_static/flask-wtf-icon.png" height="48" alt="wtform"> &nbsp;
  <img style="float: left" src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" height="48" alt="flask"> &nbsp;
  <img style="float: left" src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg" height="48" alt="docker"> &nbsp;
  <img style="float: left" src="https://code.visualstudio.com/assets/updates/1_35/logo-stable.png" height="48" alt="vscode">
</div>
