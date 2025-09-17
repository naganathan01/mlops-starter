# MLOps Starter Makefile

.PHONY: help install clean test lint format docker-build docker-run deploy-infra deploy-k8s train serve

# Default target
help:
	@echo "Available commands:"
	@echo "  install       - Install Python dependencies"
	@echo "  clean         - Clean up temporary files"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linting"
	@echo "  format        - Format code"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-run    - Run services with docker-compose"
	@echo "  deploy-infra  - Deploy infrastructure with Terraform"
	@echo "  deploy-k8s    - Deploy to Kubernetes"
	@echo "  train         - Train model locally"
	@echo "  serve         - Start inference server"

# Python environment setup
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

requirements.txt: conda.yaml
	conda env export --from-history | grep -v "^prefix:" > conda-export.yaml
	conda env create -f conda-export.yaml -n temp-env
	conda activate temp-env && pip freeze > requirements.txt
	conda env remove -n temp-env
	rm conda-export.yaml

requirements-dev.txt:
	@echo "pytest>=7.0.0" > requirements-dev.txt
	@echo "black>=23.0.0" >> requirements-dev.txt
	@echo "flake8>=6.0.0" >> requirements-dev.txt
	@echo "mypy>=1.0.0" >> requirements-dev.txt
	@echo "pre-commit>=3.0.0" >> requirements-dev.txt

# Code quality
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".coverage" -delete

test:
	pytest tests/ -v --cov=src/ --cov-report=html

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

# Docker operations
docker-build:
	docker build -t mlops-starter:latest -f docker/Dockerfile .
	docker build -t mlflow-server:latest -f docker/Dockerfile.mlflow .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

# Infrastructure deployment
deploy-infra:
	cd infra && terraform init && terraform plan && terraform apply -auto-approve

destroy-infra:
	cd infra && terraform destroy -auto-approve

# Kubernetes deployment
deploy-k8s:
	kubectl apply -f k8s/
	kubectl rollout status deployment/mlflow-server -n mlops
	kubectl rollout status deployment/model-server -n mlops

undeploy-k8s:
	kubectl delete -f k8s/

# Model operations
train:
	python src/train.py --n-estimators 100 --max-depth 10

train-mlflow:
	mlflow run . -P n_estimators=100 -P max_depth=10

serve:
	python src/inference.py

# Development helpers
dev-setup: install requirements-dev.txt
	pre-commit install

mlflow-ui:
	mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 0.0.0.0

# AWS helpers
update-kubeconfig:
	aws eks update-kubeconfig --name mlops-cluster --region us-west-2

get-pods:
	kubectl get pods -n mlops

logs-mlflow:
	kubectl logs -f deployment/mlflow-server -n mlops

logs-model:
	kubectl logs -f deployment/model-server -n mlops

# Port forwarding for local development
port-forward-mlflow:
	kubectl port-forward service/mlflow-service 5000:80 -n mlops

port-forward-model:
	kubectl port-forward service/model-server-service 8000:80 -n mlops
