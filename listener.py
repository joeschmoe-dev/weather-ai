from vosk import Model, KaldiRecognizer
import pyaudio, json
import requests, random, os, edge_tts, time, asyncio
from dotenv import load_dotenv
import os

load_dotenv()

model = Model(os.getenv("VOSKAI_MODEL"))  # Provide path to a pre-downloaded Vosk model
recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

print("Listening...")


ENDPOINT = os.getenv("API_ENDPOINT")  # Replace with the actual API endpoint

global conversation_history, user, charName, charStart

user = "User"

charName = "Weather Bot"
charStart = "Im the weatherman"
charEx = ""
charDesc = ""
startingPrompt = "[The following is an interesting chat message log between {user} and AI.]\n\n"


global temp
temp = -3




def genkey():
    n1 = str(random.randrange(0,10))
    n2 = str(random.randrange(0,10))
    n3 = str(random.randrange(0,10))
    n4 = str(random.randrange(0,10))
    return ("KCPP" + n1 + n2 + n3 + n4)

def get_prompt(user_msg, memory=""):
    return {
    "n": 1,
    "max_context_length": 1600,
    "max_length": 225,
    "rep_pen": 1.15,
    "temperature": 1.35,
    "top_p": 1,
    "top_k": 0,
    "top_a": 0,
    "typical": 1,
    "tfs": 0.69,
    "rep_pen_range": 1600,
    "rep_pen_slope": 0.1,
    "sampler_order": [
        6,
        3,
        2,
        5,
        0,
        1,
        4
    ],
    "memory": memory,
    "trim_stop": True,
    "genkey": genkey(),
    "min_p": 0,
    "dynatemp_range": 0,
    "dynatemp_exponent": 1,
    "smoothing_factor": 0,
    "banned_tokens": [],
    "render_special": False,
    "logprobs": False,
    "presence_penalty": 0,
    "logit_bias": {},
    "prompt": user_msg,
    "quiet": True,
    "stop_sequence": [
        (user + ":"),
        ("\n" + user + " "),
        ("\n" + charName + ": ")
    ],
    "use_default_badwordsids": False,
    "bypass_eos": False
}


charDesc = ""

def update_temp(temperature):
    global charDesc
    charDesc = f"""IMPORTANT:  
REGULAR CHAT RESPONSE UNLESS SPECIFICALLY ASKED ABOUT WEATHER OR TEMPERATURE.  

IF EXPLICITLY ASKED ABOUT THE WEATHER OR TEMPERATURE:  
- Respond in a weatherman style.  
- Provide only the temperature (in Fahrenheit). No windspeed or forecast.  
- Include appropriate clothing suggestions for the temperature.  

Temperature: "{temperature}°F"  
The temperature is {temperature}°F.  
"""
    #print(charDesc)
    print()
    print()


def send_to_api(prompt: str) -> str:
    """Send user message to API and return the AI-generated response."""
    try:
        response = requests.post(f"{ENDPOINT}/api/v1/generate", json=get_prompt(prompt, charDesc))
        response.raise_for_status()
        results = response.json()['results']
        text = results[0]['text']
        return text
    except Exception as e:
        
        return f"Error: {str(e)}"


import pygame
pygame.mixer.init()
if os.path.exists(os.path.join(os.getcwd(), 'output.mp3')):
    os.remove(os.path.join(os.getcwd(), 'output.mp3'))

async def text_to_speech(text: str, output_file: str = (os.path.join(os.getcwd(), 'output.mp3'))):
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    if os.path.exists(os.path.join(os.getcwd(), 'output.mp3')):
        os.remove(os.path.join(os.getcwd(), 'output.mp3'))

    communicate = edge_tts.Communicate(text.replace(".", ",").replace("!", "."), voice="en-GB-RyanNeural", rate="+25%", pitch="-4Hz", volume= "-10%")
    await communicate.save(output_file)
    time.sleep(1)
    print(f"Audio saved as {output_file}")
    pygame.mixer.music.load(os.path.join(os.getcwd(), 'output.mp3'))
    pygame.mixer.music.play()




async def SENDIT(message_text="What is the temperature?"):
    global conversation_history, user, charName, charStart
    parsed_message = ("" + user + ": " + message_text + "\n" + charName + ": ")
    if conversation_history == "":
        parsed_message = ("" + charName + ": " + charStart + "\n" + user + ": " + message_text + "\n" + charName + ": ")

        
    conversation_history = conversation_history + (parsed_message)

    ai_response = send_to_api(conversation_history)

    print("    AI RESPONSE:", ai_response)
    
    await text_to_speech(ai_response)





import serial

port = "COM3"  # Replace with your serial port
baud_rate = 9600
arduino = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)

while True:
    data = stream.read(4096)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        print(result)
        print(" ".join(json.loads(result)["text"].lower().split()[1:]))
        what_it_heard = json.loads(result)["text"]
        ##    what_it_heard[1:]
        ending = what_it_heard.lower()#" ".join(what_it_heard)
        response1 = ["what's the weather", "what is the weather", "what's the temperature", "what is the temperature"]
        response2 = ["how hot is it", "how cold is it"]
        response3 = ["what should i wear today", "what should i wear", "what should i wear outside"]
        ending2 = (" ".join(json.loads(result)["text"].lower().split()[1:]))
        if ending in response1 or ending in response2 or ending in response3 or ending2 in response1 or ending2 in response2 or ending2 in response3:
            tempReceived = False
            arduino.write(("read\n").encode('utf-8'))
            print("Requested temp...")
            while (not tempReceived):
                if arduino.in_waiting > 0:
                    received_data = arduino.readline().decode('utf-8').strip()
                    print(f"Received temp: {received_data}")
                    
                    temp = round(((float(received_data) * 9/5) + 32), 2)
                    update_temp(temp)
                    tempReceived = True

            if ending in response1 or ending2 in response1:
                #print("TRUE")
                asyncio.run(SENDIT())
            elif ending in response2 or ending2 in response2:
                asyncio.run(SENDIT("how hot/cold is it?"))
                t = 2
            elif ending in response3 or ending2 in response3:
                asyncio.run(SENDIT(("what should I wear if it's " + str(temp) + " outside?")))
            else:
                t = 2
