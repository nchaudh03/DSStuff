poetry_export:
	poetry export >> ./deploy/requirements.txt

docker_build:
	poetry export >> ./dist/requirements.txt
	docker build -f ./deploy/Dockerfile -t nchaudh03/katlib-iris:latest .

make docker_push:
	docker push nchaudh03/katlib-iris:latest

make docker_run:
	docker run --rm nchaudh03/katlib-iris:latest