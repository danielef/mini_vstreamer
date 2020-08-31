# mini-vstreamer
Mini HTTP Video Streamer

# Development
Download source code:
```
git clone https://github.com/danielef/mini_vstreamer
```

Create a virtual environment, with virtualenv:
```
cd mini_vstreamer/
virtualenv -p python3.8 venv
```

Activate your virtualenv and install dependencies:
```
source venv/bin/activate
pip install -r requirements.txt
```

Install this application in develop mode and start it:
```
python setup.py develop
python -m mini_vstreamer.app
```
