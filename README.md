# Cloud-Based Web Services through Edge-Cloud Collaboration

## Overview

This project demonstrates a cloud-native airline booking system designed using a microservices architecture. The system simulates both traditional cloud deployment and edge-cloud collaboration to analyze performance, latency, scalability, and service reliability.

The application consists of multiple independent services communicating through REST APIs and managed using Docker containers. An API Gateway acts as the entry point, while a management service provides monitoring and control capabilities.

---

## Architecture

### Services

| Service | Description |
|----------|-------------|
| API Gateway | Entry point for all client requests |
| Booking Service | Handles flight booking workflows |
| Inventory Service | Manages available seats |
| Payment Service | Simulates payment processing |
| Management Service | Monitors and controls running services |

### System Workflow

1. Client sends booking request to API Gateway.
2. API Gateway forwards request to Booking Service.
3. Booking Service checks seat availability from Inventory Service.
4. Booking Service processes payment through Payment Service.
5. Inventory Service updates seat count.
6. Booking confirmation is returned to the client.

---

## Project Structure

```text
cloud-airline-system/
│
├── services/
│   ├── api-gateway/
│   ├── booking-service/
│   ├── inventory-service/
│   ├── payment-service/
│   └── management-service/
│
├── infrastructure/
│   └── kubernetes/
│
├── docker-compose.yml
│
└── README.md
```

---

## Technologies Used

- Python
- FastAPI
- Docker
- Docker Compose
- Kubernetes
- REST APIs
- Async Programming (asyncio)
- HTTPX

---

## Features

### API Gateway
- Centralized request routing
- Cloud mode simulation
- Edge-cloud latency comparison
- CORS enabled

### Booking Service
- Booking request processing
- Service orchestration
- Communication with inventory and payment services

### Inventory Service
- Seat availability tracking
- Concurrent request handling
- Thread-safe operations

### Payment Service
- Payment processing simulation
- Network delay simulation

### Management Service
- Service monitoring
- Start/Stop/Restart containers
- Docker integration
- Runtime management APIs

---

## Docker Deployment

### Clone Repository

```bash
git clone https://github.com/your-username/Cloud-Based-Web-Services-through-Edge-Cloud-Collaboration.git

cd Cloud-Based-Web-Services-through-Edge-Cloud-Collaboration/cloud-airline-system
```

### Build and Run

```bash
docker-compose up --build
```

### Run in Background

```bash
docker-compose up -d --build
```

### Stop Services

```bash
docker-compose down
```

---

## Service Ports

| Service | Port |
|----------|------|
| API Gateway | 8001 |
| Booking Service | 8002 |
| Inventory Service | 8003 |
| Payment Service | 8004 |
| Management Service | 8005 |

---

## API Endpoints

### API Gateway

#### Get Configuration

```http
GET /config
```

#### Update Configuration

```http
POST /config
```

Request Body:

```json
{
  "cloud_mode": true
}
```

#### Book Flight

```http
POST /book
```

---

### Inventory Service

#### Check Available Seats

```http
GET /check
```

#### Consume Seat

```http
POST /consume
```

---

### Payment Service

#### Process Payment

```http
POST /pay
```

---

### Management Service

#### List Services

```http
GET /services
```

#### Start Service

```http
POST /services/{service-name}/start
```

#### Stop Service

```http
POST /services/{service-name}/stop
```

#### Restart Service

```http
POST /services/{service-name}/restart
```

---

## Kubernetes Deployment

Kubernetes manifests are available in:

```text
infrastructure/kubernetes/
```

Apply the configurations:

```bash
kubectl apply -f infrastructure/kubernetes/
```

Verify deployment:

```bash
kubectl get pods
kubectl get services
```

---

## Edge-Cloud Collaboration Simulation

The project supports two operating modes:

### Cloud Mode
- Requests travel through centralized cloud services.
- Additional latency is introduced to simulate WAN communication.

### Edge Mode
- Requests are processed closer to the user.
- Reduced response time.
- Lower network latency.

This enables comparison between traditional cloud deployments and edge-assisted architectures.

---

## Performance Objectives

- Reduce request latency
- Improve scalability
- Enhance service availability
- Demonstrate microservice orchestration
- Simulate real-world airline booking workloads

---

## Future Enhancements

- Database integration (PostgreSQL/MySQL)
- Authentication and authorization
- Service discovery
- Distributed tracing
- Load balancing
- Auto-scaling with Kubernetes
- CI/CD pipeline integration
- Real payment gateway support

---

## Authors

**Abhik Dey**

M.Tech Thesis: Cloud-Based Web Services through Edge-Cloud Collaboration

---

## License

This project is developed for academic and research purposes.
