

remove-rabbit:
	docker rm -f some-rabbit

run-rabbit: remove-rabbit
	docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management
