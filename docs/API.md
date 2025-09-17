# API Documentation

## Model Server Endpoints

### Health Check

```http
GET /health
```

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Readiness Check

```http
GET /ready
```

Returns whether the service is ready to serve requests.

**Response:**
```json
{
  "status": "ready",
  "model_version": "1"
}
```

### Make Predictions

```http
POST /predict
```

Make predictions using the loaded model.

**Request Body:**
```json
{
  "data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]],
  "feature_names": ["feature_0", "feature_1", "feature_2", "feature_3", "feature_4", "feature_5", "feature_6", "feature_7", "feature_8", "feature_9"]
}
```

**Response:**
```json
{
  "predictions": [12.34],
  "model_version": "1"
}
```

### Model Information

```http
GET /model-info
```

Get information about the currently loaded model.

**Response:**
```json
{
  "model_version": "1",
  "model_type": "RandomForestRegressor",
  "feature_count": 10
}
```

## MLflow API

MLflow provides its own REST API. See the [MLflow REST API documentation](https://mlflow.org/docs/latest/rest-api.html) for details.

### Common MLflow Endpoints

- `GET /api/2.0/mlflow/experiments/list` - List experiments
- `GET /api/2.0/mlflow/runs/search` - Search runs
- `GET /api/2.0/mlflow/model-versions/search` - Search model versions

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid request
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service not ready

Error response format:
```json
{
  "detail": "Error description"
}
```
