import speech_recognition as sr

spoken_query = None  # global variable to store the spoken query

def captureAudio(r):
    global spoken_query  # tell Python we're using the global variable

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

            try:
                transcription = r.recognize_google(audio, language="en-US")

                if "activate lexi" in transcription.lower():
                    with sr.Microphone() as source: 
                        print("Ask your question!!!")
                        source.pause_threshold = 1
                        audio = r.listen(source, timeout=10, phrase_time_limit=None)
                        try:
                            query = r.recognize_google(audio)
                            spoken_query = query  # set the global variable
                        except:
                            print("No query made. Deactivating!!!")

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

