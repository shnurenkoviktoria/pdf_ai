## Introduction
------------
The MultiPDF Chat App is a Python application that allows you to chat with multiple PDF documents. You can ask questions about the PDFs using natural language, and the application will provide relevant responses based on the content of the documents. This app utilizes a language model to generate accurate answers to your queries. Please note that the app will only respond to questions related to the loaded PDFs.

## You can use my app from this link: [pdfs-ai][1]
[1]:https://pdfs-ai.streamlit.app/ "MultiPDF Chat"


## Dependencies and Installation
----------------------------
To install the MultiPDF Chat App, please follow these steps:

1. Clone the repository to your local machine.

   Make sure you are in the correct current directory.

   if not, change the directory to the correct one:
   ```bash
   cd <path_to_directory>.
   ```
    Then run one of the following command:
    ```bash
   pip install git+https://github.com/shnurenkoviktoria/pdf_ai.git
   ```
   or
   ```bash
    git clone https://github.com/shnurenkoviktoria/pdf_ai.git
    ```
   or download the zip file and extract it to the desired directory.
   

2. Install the required dependencies by running the following command:
   ```bash
   pip install -r requirements.txt
   ```

3. Obtain an API key from OpenAI and add it to the `.env` file in the project directory.
   ```commandline
   OPENAI_API_KEY = your_secrit_api_key
   ```

## Usage
-----
To use the MultiPDF Chat App, follow these steps:

1. Ensure that you have installed the required dependencies and added the OpenAI API key to the `.env` file.
   ```bash
   cd <path_to_directory>.
   ```

2. Run the `main.py` file using the Streamlit CLI. Execute the following command:
   ```bash
   streamlit run pdfs.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Load multiple PDF documents into the app by following the provided instructions.

5. Ask questions in natural language about the loaded PDFs using the chat interface.
