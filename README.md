# Sentiment analysis API

A small api for sentiment analysis (TextBlob in the background) encapsulated in docker.

## Live demo

Check this [demo](http://guillim-sentiment-analysis-api.herokuapp.com/documentation/) to see this tool in action !
(Thanks Heroku for hosting it)



## Install


```sh
git clone https://github.com/guillim/sentiment_analysis_api.git api
```


## Launch

**You must have docker installed to make this work**

```
cd api
make up
```

In your browser, go to [localhost:5000/status](http://localhost:5000/status) and it should print

```
{
    "status":"connected"
}
```


## Use

Then you can use the API to send some text and receive the sentiment analysis. We present two ways: Curl and Swagger. Feel free to use postman or anything else to make your calls.

#### Curl

```bash
curl -X POST \
  http://guillim-sentiment-analysis-api.herokuapp.com/sentiment \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \ 
  -d '{ 
        "analyzer": "PatternAnalyzer", 
	"text": "Paris is a nice city to live in. I like New york as well, but Paris has a charm you cannot find elsewhere"
  }'  
```


Returns:


```
{
  "sentiment": "positive",
  "sentiment_score": [
    0.2909090909090909,
    0.6515151515151515
  ],
  "detected_language": "en",
  "message": ""
}
```

#### Swagger

Go to [localhost:5000/documentation](http://localhost:5000/documentation) and you will have an interactive tool for testing

## Documentation

Go to [localhost:5000/documentation](http://localhost:5000/documentation) for any question about paramters availables, options etc...

## Deploy on Heroku

Go to the ``` Heroku Container Registry ``` option for the available commands to trigger from your local folder. Can't use Git integration since it is a docker-compose based app

```bash
heroku container:login  
heroku container:push web  
heroku container:release web
```

## License

Copyright © 2019 Guillaume Lancrenon
Distributed under MIT licence.
