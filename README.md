# Documentation for RAG_API Project

## Overview

RAG_API is a RESTful API designed for researching and retrieving documents based on semantic similarity. It utilizes FastAPI for the web framework, Pydantic for data validation, and integrates Ollama for natural language understanding and embeddings. This API allows users to upload documents and search for similar documents based on their content.

## Features

- **File Upload**: Users can upload documents to be indexed and later retrieved through semantic search.
- **Semantic Search**: Leveraging Ollama embeddings, users can perform queries to find documents that are semantically similar to their search terms.

## Technology Stack

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Ollama**: For utilizing language models and generating embeddings.
- **Qdrant**: A vector search engine for storing and searching embeddings.
- **YAML**: For configuration management.
- **aiofiles**: For asynchronous file operations.

## Setup

### Prerequisites

- Python 3.7+
- Pip for Python package installation.








### Installation Steps

1. Clone the repository to your local machine.


2. Install the required Python packages using poetry:
   ```
   poetry install
   ```

3. Configure your `config.yml` file according to your setup, specifying the necessary parameters for the language model, Qdrant settings, and embedding model.

### Running the API
#### starts ollama server
   ```
   docker run -p 6333:6333   qdrant/qdrant:latest
   ```
#### starts qdrant server
   ```
   docker run -p 6333:6333   qdrant/qdrant:latest
   ```

#### run fastapi app
Execute the following command to run the API server:
```
python app.py
```

## API Endpoints

### Root Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a welcome message from the API.

### Upload File

- **URL**: `/uploadfile/`
- **Method**: `POST`
- **Description**: Allows users to upload a file for indexing.
- **Body**: `multipart/form-data` with a file field.

### Search

- **URL**: `/search/`
- **Method**: `POST`
- **Description**: Performs a semantic search on the indexed documents.
- **Body**:
  ```json
  {
    "query": "Your search query",
    "similarity_top_k": 3
  }
  ```
  - `query`: The search query.
  - `similarity_top_k`: Optional. The number of top similar documents to retrieve. Defaults to 1.

## Models

### Query Model

Defines the structure for the search query input.

### Response Model

Defines the structure of the search response, including the search result and source document information.

## Development

### Adding New Features

To contribute or extend the API, follow the project's coding standards and submit pull requests for review.

### Testing

Implement unit tests for new features and run existing tests to ensure stability.

## Support and Contribution

For support, please open an issue on the GitHub repository. Contributions are welcome and should be submitted via pull requests.

## License

####