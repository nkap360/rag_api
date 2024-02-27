# RAG API Documentation

## Introduction

Welcome to the RAG API, a Rest API designed to facilitate the indexing and querying of documents using state-of-the-art vector search technology. This project is built on FastAPI and leverages Qdrant for vector storage and retrieval, combined with the power of language models for embedding generation. It is intended for developers and researchers looking to integrate advanced search capabilities into their applications.

## Features

- **Document Indexing**: Easily index your documents for vector-based searching.
- **Efficient Querying**: Leverage the speed of Qdrant and the accuracy of language models to quickly find relevant documents.
- **Scalable and Flexible**: Designed to handle a large number of documents and easily integrate into existing systems.

## Installation

Ensure you have Python 3.10 or newer installed on your system. This project uses Poetry for dependency management.

1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/yourrepository/rag_api.git
   cd rag_api
   ```
2. Install the required dependencies using Poetry.
   ```bash
   poetry install
   ```

## Configuration

Before running the API, configure it by editing the `config.yaml` file in the root directory. Here are the available configuration options:

- `llm`: Specify the language model used for embeddings.
- `embedding`: The embedding model for vector generation.
- `qdrant_local`: The URL of your Qdrant server.
- `qdrant_timeout`: Timeout in seconds for Qdrant requests.
- `collection_name`: The name of the collection in Qdrant where documents will be stored.
- `chunk_size`: Size of chunks for processing documents.
- `upload_dir`: Directory where uploaded files will be saved.
- `openai_api_key`: Your OpenAI API key for language model access.

Replace placeholder values with your actual configuration details.

## Running the Application
After configuring your environment, start the API server with the following command:
### starts ollama server
   ```
    
   ```
### starts qdrant server
   ```
   docker run -p 6333:6333   qdrant/qdrant:latest
   ```

### run fastapi app
Execute the following command to run the API server:
```bash
python app.py
```

This command starts the FastAPI server with hot reload enabled, making it suitable for development.

## API Usage

The API provides endpoints for uploading documents and querying the indexed content.

### Uploading Documents

To upload a document for indexing, head to http://127.0.0.1:8000/docs# 
or send a POST request to `/upload` with the file as multipart/form-data. The document will be processed, indexed, and made searchable.

```bash
curl -X 'POST' \
  'http://localhost:8000/upload' \
  -F 'file=@path_to_your_document'
```

### Querying the Index

To search through the indexed documents, head to http://127.0.0.1:8000/docs# 
or send a GET request to `/search` with your query parameters. Specify your search query to find relevant documents.

```bash
curl -X 'GET' \
  'http://localhost:8000/search?query=your_search_query'
```

## Development and Contribution

Contributions to the RAG API are welcome! Whether you're fixing bugs, adding new features, or improving the documentation, your help is appreciated.

- **Submit Pull Requests**: Fork the repository, make your changes, and submit a pull request.
- **Report Issues**: If you find bugs or have feature requests, please open an issue on GitHub.
- **Suggestions**: We're always looking for feedback to improve the project.

## Contact and Support

For support, questions, or more information, please open an issue on the GitHub repository. We aim to respond to queries promptly and welcome your feedback to improve the RAG API.

## License

[MIT License](LICENSE.txt) - Feel free to use, modify, and distribute this software as per the license terms.

## Conclusion

Thank you for your interest in the RAG API. We hope this documentation helps you get started with the project. For further assistance or to contribute, don't hesitate to reach out through our support channels or GitHub repository.
```

This template is designed to be comprehensive and cover all necessary aspects to get started with the project, including installation, configuration, running the application, API usage, and contributing guidelines. Ensure to replace placeholder links and values with the actual data relevant to your project.