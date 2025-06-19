# Tech Test Boilerplate

A comprehensive Python boilerplate for technical interviews and coding challenges, featuring Docker and Kubernetes integration.

[![Maintainability](https://qlty.sh/badges/093ec62a-41e0-4919-8598-73ccaed85597/maintainability.svg)](https://qlty.sh/gh/Little-mighty-developer/projects/tech_test_boilerplate)

[![Code Coverage](https://qlty.sh/badges/093ec62a-41e0-4919-8598-73ccaed85597/test_coverage.svg)](https://qlty.sh/gh/Little-mighty-developer/projects/tech_test_boilerplate)

# 📊 Developer Experience Metrics

## 🚀 Features

- **Code Quality**

  - Black for code formatting
  - Flake8 for linting
  - MyPy for type checking
  - Pre-commit hooks for automated checks

- **Testing**

  - Pytest for unit testing
  - Pytest-cov for coverage reporting
  - FastAPI for API development

- **Containerization & Orchestration**

  - Docker support
  - Kubernetes deployment
  - Health checks
  - Resource management

- **Development Environment**
  - Python 3.11
  - Virtual environment support
  - Environment variable management
  - Development tools configuration

git clone <repository-url>

cd tech_test_boilerplate


````

2. Create and activate virtual environment:

```bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
````

3. Install dependencies:

```bash

```

4. Install pre-commit hooks:

pre-commit install

````
5. Set up environment variables:

```bash
cp .env.example .env
````

## 🛠️ Available Commands

- `pytest` - Run tests
- `pytest --cov` - Run tests with coverage

- `black .` - Format code
- `flake8` - Run linting
- `mypy .` - Run type checking
- `pre-commit run --all-files` - Run all pre-commit hooks

## 🐳 Docker

Build and run the Docker container:

````bash
docker build -t tech-test-app .
docker run -p 8000:8000 tech-test-app

## ☸️ Kubernetes

Deploy to Kubernetes:

```bash
kubectl apply -f k8s/deployment.yaml
````

## 📁 Project Structure

```
├── src/                    # Source code
├── tests/                  # Test files
├── k8s/                   # Kubernetes configurations
├── .pre-commit-config.yaml # Pre-commit hooks
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
