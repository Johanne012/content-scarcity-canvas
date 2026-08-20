.PHONY: up down init apply destroy seed test logs clean all

ENDPOINT ?= http://localhost:4566

up:
	docker compose up -d
	@echo "Waiting for LocalStack..."
	@sleep 5
	@curl -s $(ENDPOINT)/_localstack/health | python3 -m json.tool || true

down:
	docker compose down

init:
	terraform init

apply:
	terraform apply -auto-approve

destroy:
	terraform destroy -auto-approve

seed:
	chmod +x scripts/seed_products.sh
	PRODUCTS_TABLE=$$(terraform output -raw products_table) \
	PRODUCTS_BUCKET=$$(terraform output -raw products_bucket) \
	LOCALSTACK_ENDPOINT=$(ENDPOINT) \
	./scripts/seed_products.sh

test:
	chmod +x scripts/test_flow.sh
	./scripts/test_flow.sh $$(terraform output -raw create_order_url)

logs:
	docker compose logs -f localstack

clean:
	rm -rf build .terraform terraform.tfstate* localstack-data
	docker compose down -v || true

all: up init apply seed test
