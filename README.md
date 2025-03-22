
# File Search Chatbot

This project is a simple web application that allows users to upload files and interact with a chatbot that can answer questions based on the uploaded files. The application is built using Flask and integrates file handling and chatbot functionalities.

## Features

- Upload files from local storage or via URLs.
- Chatbot functionality to answer questions based on the content of the uploaded files.
- User-friendly interface for file uploads and chatbot interactions.

## Project Structure

```
file-upload-chatbot
├── static
│   ├── js
│   │   └── main.js
│   └── css
│       └── style.css
├── templates
│   ├── base.html
│   └── index.html
├── app.py
├── uploads
├── utils
│   ├── __init__.py
│   ├── file_handler.py
│   └── chat_handler.py
├── requirements.txt
├── .env
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd openai-file-search-chatbot
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in the `.env` file.

## Usage

1. Run the application:
   ```
   python src/app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Use the interface to upload files and interact with the chatbot.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.
