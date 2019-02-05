# Name of the repo
REPO=jeroenvo

# Name of the image
IMAGE=parcelspot-rpi

# Current branch-commit (example: master-ab01c1z)
CURRENT=`echo $$TRAVIS_BRANCH | cut -d'/' -f 2-`-$$(git rev-parse HEAD | cut -c1-7)

# Colors
GREEN=\033[0;32m
NC=\033[0m

docker: build push

build:
	echo "$(GREEN)--- BUILDING DOCKER IMAGE ---$(NC)"
	docker build -t $(REPO)/$(IMAGE):$(CURRENT) .

push:
	echo "$(GREEN)--- PUSHING IMAGE TO HUB ---$(NC)"
	docker push $(REPO)/$(IMAGE):$(CURRENT)
