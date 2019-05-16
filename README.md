# Sentiment analysis API

A small api for sentiment analysis encapsulated in docker.

## Live demo

Check this [demo](http://sentiment-analysis-api.herokuapp.com/documentation/) to see this tool in action !
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
  http://127.0.0.1:5000/sentiment \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"text": "Paris est la capitale de la France. L’agglomération de Paris compte plus de 10 millions d’habitants. Un fleuve traverse la capitale française, c’est la Seine. Dans Paris, il y a deux îles :  l’île de la Cité et l’île Saint-Louis.Paris compte vingt arrondissements. Le 16e, le 7e et le 8e arrondissements de Paris sont les quartiers les plus riches. Ils sont situés dans l’ouest de la capitale. Les quartiers populaires comme le 19e et le 20e sont au nord-est de la ville. Les monuments célèbres, les ministères, le palais de l’Élysée sont situés dans le centre de Paris.Paris est la capitale économique, la capitale politique et la capitale culturelle de la France. La ville compte beaucoup de lieux célèbres dans le monde entier comme « la tour Eiffel » , « l’Arc de Triomphe » et « Notre-Dame de Paris ». Les musées parisiens aussi sont très connus. Il y a, par exemple, le musée du Louvre. C’est le plus grand musée de France. On peut voir dans le musée du Louvre des tableaux magnifiques. Le plus célèbre est certainement « La Joconde » de Léonard de Vinci.Paris est une ville très touristique. Chaque année, des millions de touristes du monde entier marchent sur les amps-Élysées. Ils séjournent à l’hôtel, louent des chambres d’hôtes ou des appartements pour une semaine."
}'
 ```


Returns:


```
to be completed  
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
