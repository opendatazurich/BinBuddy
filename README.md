# BinBuddy

## Demo

[![Watch the demo](https://img.youtube.com/vi/MUNdhnGGVCI/default.jpg)](https://youtu.be/MUNdhnGGVCI)

## Datasets

Gemeinden: https://s.zazuko.com/2cdhrjj
Feiertage: 

CSV-Format: https://github.com/metaodi/openerz/tree/main/csv#format

## Flask application

To run the application:

```
python app.py
```

The vue app is in the `bin-buddy/src` directory.

To run the vue app:

```
cd client
npm run serve
```


# Setup

To setup python run:

```
./python_setup.sh
```

To setup the vue application:

```
cd bin-buddy
npm install
```

The application needs a Persal Access Token of GitHub, please provide it in your `.env` file:

```
cp .env.dist .env
# edit .env
```
