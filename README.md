# Decen 🛡️

A Decentralized Content Moderation Platform powered by AI and Blockchain technology.

## Overview 🌟

Decen is an innovative content moderation platform that combines the power of artificial intelligence with blockchain technology to provide transparent, efficient, and decentralized content moderation services. Perfect for social media platforms, news websites, forums, and any platform requiring content moderation.

## Features ✨

- **AI-Powered Content Analysis** 🤖

  - Text content moderation
  - Image content moderation
  - Text extraction from images
  - Multi-category classification
  - Batch processing support

- **Blockchain Integration** ⛓️

  - Immutable moderation records
  - Transparent decision history
  - Decentralized storage
  - Verifiable moderation results

- **Secure API** 🔒

  - JWT authentication
  - Role-based access control
  - CORS support
  - Rate limiting

- **Developer Friendly** 💻
  - OpenAPI documentation
  - Easy-to-use REST API
  - Modular architecture
  - Comprehensive error handling

## Technology Stack 🛠️

- **Backend Framework**: FastAPI
- **AI/ML**: TensorFlow, Transformers
- **Blockchain**: Web3.py
- **Image Processing**: OpenCV, Pillow
- **OCR**: Pytesseract
- **Authentication**: JWT
- **Documentation**: OpenAPI/Swagger

## Getting Started 🚀

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)
- Ethereum node access (for blockchain features)

### Installation

1. Clone the repository:

```bash
cd decen
```

2. Create and activate virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file:

```env
BLOCKCHAIN_PROVIDER_URL=your_provider_url
SMART_CONTRACT_ADDRESS=your_contract_address
SECRET_KEY=your_secret_key
MODEL_PATH=path_to_your_ai_model
```

### Running the Application

1. Start the server:

```bash
python main.py
```

2. Access the API documentation:

- OpenAPI UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Usage 📡

### Authentication

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=secret"
```

### Content Moderation

Text moderation:

```bash
curl -X POST "http://localhost:8000/api/v1/moderation/text" \
     -H "Authorization: Bearer your_token" \
     -H "Content-Type: application/json" \
     -d '{"content": "Your text here", "content_type": "text"}'
```

Image moderation:

```bash
curl -X POST "http://localhost:8000/api/v1/moderation/image" \
     -H "Authorization: Bearer your_token" \
     -F "file=@path_to_image.jpg"
```

## Project Structure 📁

```
.
├── app/
│   ├── core/           # Core configuration and security
│   ├── api/            # API routes and dependencies
│   ├── services/       # Business logic services
│   ├── models/         # Data models and schemas
│   └── utils/          # Utility functions
├── main.py            # Application entry point
└── requirements.txt   # Project dependencies
```

## Contributing 🤝

We welcome contributions! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact 📧

[Twitter](https://x.com/Decen_Sys)

## Acknowledgments 🙏

- OpenAI for AI models
- Ethereum community
- FastAPI team
- All contributors and supporters
