up-prod:
	docker-compose -f docker-compose.prod.yml up -d --build

down-prod:
	docker-compose -f docker-compose.prod.yml down