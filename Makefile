# Name of the repo
REPO=jeroenvo

# Name of the image
IMAGE=parcelspot-rpi

# Current branch-commit (example: master-ab01c1z)
CURRENT=`echo $$TRAVIS_BRANCH | cut -d'/' -f 2-`-$$(git rev-parse HEAD | cut -c1-7)

# Colors
GREEN=\033[0;32m
NC=\033[0m

build:
	echo "$(GREEN)--- BUILDING DOCKER IMAGE ---$(NC)"
	docker build -t $(REPO)/$(IMAGE):$(CURRENT) .

push:
	echo "$(GREEN)--- PUSHING IMAGE TO HUB ---$(NC)"
	docker push $(REPO)/$(IMAGE):$(CURRENT)

deploy-api:
	echo "$(GREEN)--- DEPLOYING API TO SERVER ---$(NC)"
	node operations/scripts/deploy.js --sshPassword $$SSH_PASSWORD --sshUser $$SSH_USER --tag $(CURRENT) --dockerUsername $$DOCKER_USERNAME --dockerPassword $$DOCKER_PASSWORD --image $(IMAGE) --port 8081:8081
