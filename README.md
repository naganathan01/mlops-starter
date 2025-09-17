# MLOps Starter Project

A comprehensive MLOps starter template with MLflow, Kubernetes, and AWS infrastructure.

## 🏗️ Architecture

- **Infrastructure**: AWS EKS, S3, RDS (managed with Terraform)
- **Model Tracking**: MLflow for experiment tracking and model registry
- **Model Serving**: FastAPI-based model server deployed on Kubernetes
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Containerization**: Docker for consistent environments

## 📁 Project Structure

```
mlops-starter/
├── infra/           # Terraform infrastructure code
├── k8s/             # Kubernetes manifests
├── docker/          # Docker configurations
├── src/             # Python source code
├── .github/         # GitHub Actions workflows
└── docs/            # Documentation
```

## 🚀 Quick Start

### Prerequisites

- AWS CLI configured
- Docker installed
- kubectl configured
- Terraform installed
- Python 3.9+

### 1. Infrastructure Setup

```bash
# Deploy infrastructure
cd infra
terraform init
terraform plan
terraform apply
```

### 2. Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MLflow server locally
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts

# Train model
python src/train.py --n-estimators 100 --max-depth 10

# Start inference server
python src/inference.py
```

### 3. Kubernetes Deployment

```bash
# Update kubeconfig
aws eks update-kubeconfig --name mlops-cluster --region us-west-2

# Deploy MLflow and model server
kubectl apply -f k8s/

# Check deployments
kubectl get pods -n mlops
```

## 🔧 Configuration

### Environment Variables

- `MLFLOW_TRACKING_URI`: MLflow server URL
- `MODEL_NAME`: Name of the registered model
- `MODEL_VERSION`: Version of the model to serve
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key

### Secrets

Update `k8s/mlflow-secret.yaml` with your actual values:

```yaml
stringData:
  backend-store-uri: "postgresql://user:pass@host:5432/db"
  artifact-root: "s3://your-bucket"
  aws-access-key-id: "your-key"
  aws-secret-access-key: "your-secret"
```

## 📊 Model Training

```bash
# Basic training
python src/train.py

# With custom parameters
python src/train.py --n-estimators 200 --max-depth 15

# Using MLflow project
mlflow run . -P n_estimators=100 -P max_depth=10
```

## 🎯 Model Serving

The inference service provides REST API endpoints:

- `GET /health` - Health check
- `GET /ready` - Readiness check  
- `POST /predict` - Make predictions
- `GET /model-info` - Model information

Example request:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}'
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow:

1. **Test**: Runs linting, formatting, and tests
2. **Build**: Creates Docker image and pushes to registry
3. **Deploy**: Updates Kubernetes deployment

## 📝 Development Workflow

1. Create feature branch
2. Make changes and test locally
3. Push changes (triggers CI)
4. Create pull request
5. Merge to main (triggers deployment)

## 🛠️ Customization

### Adding New Models

1. Update `src/train.py` with your model
2. Modify `src/inference.py` for serving
3. Update `conda.yaml` with dependencies
4. Test locally and deploy

### Infrastructure Changes

1. Modify Terraform files in `infra/`
2. Plan and apply changes
3. Update Kubernetes configs if needed

## 📚 Documentation

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🔍 Monitoring

### MLflow UI
Access at: `http://mlflow.yourdomain.com`

### Model Server Metrics
- Health: `GET /health`
- Metrics: Available via Prometheus endpoints (add monitoring setup)

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/

# Run specific test
pytest tests/test_inference.py
```

## 🚨 Troubleshooting

### Common Issues

1. **Model loading fails**
   - Check MLflow tracking URI
   - Verify model name and version
   - Check AWS credentials

2. **Kubernetes deployment issues**
   - Verify cluster connection: `kubectl cluster-info`
   - Check pod logs: `kubectl logs -f deployment/mlflow-server -n mlops`
   - Verify secrets: `kubectl get secrets -n mlops`

3. **Infrastructure deployment fails**
   - Check AWS credentials and permissions
   - Verify region settings
   - Check Terraform state

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
