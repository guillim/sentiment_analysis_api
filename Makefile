export APP=sentiment_api
export DC_PREFIX= $(shell pwd)/docker-compose

#other variable definition
DC    := 'docker-compose'

api:
	${DC} -f ${DC_PREFIX}-api.yml up --build -d

api-log:
	${DC} -f ${DC_PREFIX}-api.yml logs --build -d

api-stop:
	${DC} -f ${DC_PREFIX}-api.yml down

up: api

down: api-stop

restart: down up
