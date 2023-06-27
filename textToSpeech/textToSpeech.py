from elevenlabs import generate, stream , play
import argparse
import json
import os

if os.path.exists('textToSpeech\\xi_config.json'):
    with open('textToSpeech\\xi_config.json', 'r') as f:
        config = json.load(f)
else:
    raise FileNotFoundError('The configuration file "config.json" does not exist.')


parser = argparse.ArgumentParser(description="configuring elevenlabs text to speech api") 
parser.add_argument('--voice_id' , default=config.get('voice_id' , '0') , help='Choose the id of voice from voices key in xi_config')
parser.add_argument('--model' , default=config.get('model' , 'eleven_monolingual_v1') , help="select eleven_monolingual_v1 for english and eleven_multilingual_v1 for other languages")
parser.add_argument('--stream' , default=config.get('stream' , True) , help='Add this tag for long responses')
args = parser.parse_args()

def Speech(text):
    audio = generate(
    api_key= os.getenv('ELEVEN_API_KEY'),
    text=text,
    voice=config['voices'][config['voice_id'] - 1],
    model=config['model'],
    stream=config['stream']
    )
    if config['stream']:
        stream(audio)
    else:
        play(audio)


if __name__ == '__main__':

    args_dict = vars(args)
    for key in args_dict.keys():
        config[key] = args_dict[key]

    with open('textToSpeech\\xi_config.json' , 'w') as f:
        json.dump(config , f , indent=4)
    
    Speech("My name is Parijat Chatterjee and I am a ML and AI developer")