# LexiBrowse - Advanced AI Document Exploration ChatBot

Welcome to LexiBrowse, your AI-powered personal assistant for fast and accurate exploration of documents. Built with the robustness of OpenAI's GPT-3 and GPT-4 models, Lexi offers precise and high-quality responses to your queries based on the document(s) at hand.

## Key Features

1. **Unlimited Document Handling**: Lexi can work with an infinite number of files, both local and from web URLs. All document embeddings are stored locally, ensuring an instant and fluid chat experience.
2. **Customizable Models**: You have the freedom to choose your preferred GPT and embedding models.
3. **Persistent Memory**: Lexi employs memory persistence, leveraging previous interactions to provide more accurate and contextual answers.
4. **Conversation Recording**: Every conversation with Lexi gets recorded in a `conversation.json` file. This feature can be instrumental in generating high-quality reports or documents, such as dissertations, research papers, and more.

## Getting Started

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

### Setup Guide

1. **Create a Virtual Environment**:

   Choose a suitable directory for your project. Navigate to this directory via the command line and run the following command to create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

   Replace `venv` with your desired name for the virtual environment.

2. **Activate the Virtual Environment**:

   Activate the environment using:

   - Windows:

     ```bash
     venv\Scripts\activate
     ```
   - Unix or MacOS:

     ```bash
     source venv/bin/activate
     ```

3. **Install Required Packages**:

   With your virtual environment activated, install necessary packages using pip. A `requirements.txt` file is provided for ease of installation:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up OpenAI API Key**: 

   To utilize the OpenAI GPT API, you must add your OpenAI API Key. [Follow this link to create one](https://platform.openai.com/account/api-keys), and then add it to the `.env` file:

   ```env
   OPENAI_API_KEY='your-api-key-here'
   ```

5. **Generate and Store Embeddings**: 

   Run the `setup.py` file to generate embeddings. Ensure you have added documents to the `input_dir` path specified in the `config.json` file (default location: `resources\pdf_files`). You can also use `python setup.py --help` to learn more about configuration options.

6. **Start the Chat Interface**: 

   Execute the `main.py` file to start the chatbot. This action will initiate Lexi, who will respond to your prompts along with references to the document and page numbers that inform her responses.

## Demo

This repository includes three research papers on deep reinforcement learning for demonstration purposes. Here's how you can get started:

1. Run the setup file:

   ```bash
   python setup.py
   ```

   ![Setup image](images/setup.png)

2. Start the chatbot:

   ```bash
   python main.py
   ```

   ![Chatbot image](images/main.png)

For any issues or further queries, feel free to open an issue or submit a pull request. Happy exploring with LexiBrowse!