README.md:

"
# LexiBrowse - Advanced AI Document Exploration ChatBot with Text-to-Speech Feature

Welcome to LexiBrowse, your AI-powered personal assistant for fast and accurate exploration of documents. Built with the robustness of OpenAI's GPT-3 and GPT-4 models, Lexi offers precise and high-quality responses to your queries based on the document(s) at hand. Now with the addition of Text-to-Speech feature, you can listen to Lexi's responses!

## Key Features

1. **Unlimited Document Handling**: Lexi can work with an infinite number of files, both local and from web URLs. All document embeddings are stored locally, ensuring an instant and fluid chat experience.
2. **Customizable Models**: You have the freedom to choose your preferred GPT and embedding models.
3. **Persistent Memory**: Lexi employs memory persistence, leveraging previous interactions to provide more accurate and contextual answers.
4. **Conversation Recording**: Every conversation with Lexi gets recorded in a `conversation.json` file. This feature can be instrumental in generating high-quality reports or documents, such as dissertations, research papers, and more.
5. **Text-to-Speech Feature**: Listen to Lexi's responses with our new text-to-speech feature, powered by the Elevenlabs API. 

## Getting Started

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)
- FFmpeg, FFplay and MPV installed (for the Text-to-Speech feature)

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

4. **Set Up OpenAI and Elevenlabs API Key**: 

   To utilize the OpenAI GPT and Elevenlabs API, you must add your OpenAI API Key and Elevenlabs API Key. [Follow this link to create an OpenAI API key](https://platform.openai.com/account/api-keys), and [Follow this link to create an Eleven labs API key](https://beta.elevenlabs.io/). Then add it to the `.env` file:

   ```env
   OPENAI_API_KEY='your-openai-api-key-here'
   ELEVEN_API_KEY='your-elevenlabs-api-key-here'
   ```

5. **Installing FFmpeg, FFplay and MPV**:

   The text-to-speech feature requires FFmpeg, FFplay and MPV to be installed on your system. You can download FFmpeg and FFplay from the [official FFmpeg website](https://ffmpeg.org/download.html) and MPV from the [official MPV website](https://mpv.io/installation/). Make sure to add them to your system's PATH.

6. **Generate and Store Embeddings**: 

   Run the `setup.py` file to generate embeddings. Ensure you have added documents to the `input_dir` path specified in the `config.json` file (default location: `resources\pdf_files`). You can also use `python setup.py --help` to learn more about configuration options

7. **Start the Chat Interface with Text-to-Speech**: 

   Execute the `main.py` file to start the chatbot. This action will initiate Lexi, who will respond to your prompts along with references to the document and page numbers that inform her responses. For disabling the text-to-speech feature, use the `--nottp` flag:

   ```bash
   python main.py --nottp
   ```

   If the Text-to-Speech feature is enabled, you will be able to hear Lexi's responses. Make sure you've configured your desired voice in the `textToSpeech\\xi_config.json` file.
