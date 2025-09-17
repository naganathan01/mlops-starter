# Deployment Guide

## Prerequisites

1. AWS CLI configured with appropriate permissions
2. kubectl installed and configured
3. Terraform >= 1.0
4. Docker installed

## Infrastructure Deployment

### 1. Set up Terraform Variables

Create `infra/terraform.tfvars`:

```hcl
region = "us-west-2"
project_name = "mlops-starter"
cluster_name = "mlops-cluster"
db_password = "your-secure-password"
```

### 2. Deploy Infrastructure

```bash
cd infra
terraform init
terraform plan
terraform apply
```

This will create:
- EKS cluster
- S3 bucket for artifacts
- RDS PostgreSQL instance
- VPC and networking
- IAM roles and policies

## Application Deployment

### 1. Update Kubeconfig

```bash
aws eks update-kubeconfig --name mlops-cluster --region us-west-2
```

### 2. Configure Secrets

Update `k8s/mlflow-secret.yaml` with actual values:

```bash
# Get RDS endpoint from Terraform outputs
terraform output rds_endpoint

# Get S3 bucket name
terraform output s3_bucket_name
```

### 3. Deploy to Kubernetes

```bash
kubectl apply -f k8s/
```

### 4. Verify Deployment

```bash
# Check pod status
kubectl get pods -n mlops

# Check services
kubectl get svc -n mlops

# View logs
kubectl logs -f deployment/mlflow-server -n mlops
```

## Accessing Services

### MLflow UI

```bash
# Port forward to access locally
kubectl port-forward service/mlflow-service 5000:80 -n mlops
```

Access at: http://localhost:5000

### Model Server

```bash
# Port forward to access locally
kubectl port-forward service/model-server-service 8000:80 -n mlops
```

Test endpoint:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"data": [[1,2,3,4,5,6,7,8,9,10]]}'
```

## Scaling

### Horizontal Pod Autoscaling

```bash
kubectl autoscale deployment model-server --cpu-percent=70 --min=2 --max=10 -n mlops
```

### Cluster Autoscaling

Update the node group configuration in Terraform.

## Monitoring

### Prometheus and Grafana (Optional)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

## Troubleshooting

### Common Issues

1. **Pod stuck in Pending**
   ```bash
   kubectl describe pod <pod-name> -n mlops
   ```

2. **Service not accessible**
   ```bash
   kubectl get endpoints -n mlops
   ```

3. **MLflow connection issues**
   - Check database connectivity
   - Verify S3 bucket permissions
   - Check AWS credentials in secrets
