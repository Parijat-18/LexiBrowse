import os
import json
import time
import argparse
import itertools
import threading
from dotenv import load_dotenv
from utils import fileDirToDoc , docToChunks , setupPersistChromaDB , linkToDoc

if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        config = json.load(f)
else:
    raise FileNotFoundError('The configuration file "config.json" does not exist.')

parser = argparse.ArgumentParser(description='Custom split and embeddings for setting up the documents for the ChromaDB')
parser.add_argument('--input_dir', type=str, default=config.get('input_dir', 'resources\pdf_files'), help='Path to the location of your documents')
parser.add_argument('--pdf_links', type=str, default="", help='list of link to pdf files')
parser.add_argument('--chunk_size', type=int, default=config.get('chunk_size', 1000), help='The size of the chunks to be used for the embedding')
parser.add_argument('--chunk_overlap' , type=int, default=config.get('chunk_overlap', 100), help='The overlap of the chunks to be used for the embedding')
parser.add_argument('--persist_dir', type=str, default=config.get('persist_dir', 'resources\db'), help='Path to the location of your persisted Chroma database')
parser.add_argument('--embedding_model' , type=str, default=config.get('embedding_model', 'text-embedding-ada-002'), help='Select the embedding model from OpenAI embeddings API')
parser.add_argument('--model' , type=str, default=config.get('model', 'gpt-3.5-turbo'), help='Select the model from OpenAI API')

if __name__ == '__main__':

    args = parser.parse_args()
    args_dict = vars(args)
    load_dotenv(".env")

    if os.getenv('OPENAI_API_KEY') == 'your-openai-api-key-here':
        print('\nWARNING: OpenAI API Key missing. Please add it to the .env file and rerun the setup')
    else:
        print('\nopenai api key setup successful!')

    if os.getenv('ELEVEN_API_KEY') == 'your-elevenlabs-api-key-here':
        print('\nWARNING: Eleven Labs API Key missing. Please add it to the .env file and rerun the setup\n')
    else:
        print('\nEleven Labs api key setup successful! API KEY\n')

    with open('config.json', 'w') as f:
        json.dump(args_dict, f , indent=4)
    print("Configuration file updated. Here's the updates config: \n" , json.dumps(args_dict, indent=4))
    def animate_process(process_name):
        for c in itertools.cycle(['.  ', '.. ', '...']):
            if done:
                break
            print(f'\r{process_name}{c}', end='', flush=True)
            time.sleep(0.3)
        print(f'\r{process_name} Successful!')

    done = False
    t = threading.Thread(target= animate_process, args=('Generating embeddings',))
    t.start()
    try:
        doc = []
        doc = fileDirToDoc(input_dir = args.input_dir)
        doc += linkToDoc(pdf_links= args.pdf_links.split(' '))
        texts = docToChunks(doc , chunk_size= args.chunk_size ,  chunk_overlap= args.chunk_overlap)
        setupPersistChromaDB(texts , persist_directory= args.persist_dir ,  embedding_model= args.embedding_model)

        done = True
    except Exception as e:
        done = True
        print(f"An error occurred while generating the embeddings: {e}")

    t.join()

    print('\nSetup complete! Now run "python main.py" to initialize Lexi.')


