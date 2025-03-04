# Weather-AI

This project integrates an **Elegoo Arduino Mega** with an **AHT21 temperature sensor** to collect real-time temperature data, which is then processed into a natural-language weather report by a **locally hosted LLM using KoboldAI**. A Python script facilitates communication between the Arduino and the AI model while also utilizing **VoskAI** for speech recognition and **Pygame** for text-to-speech output.

## How It Works

1. **Arduino Mega with AHT21 Sensor**: The Arduino Mega remains idle until it receives a serial request from the Python script. Once requested, it fetches the temperature in Celsius from the AHT21 sensor and sends it back via serial.
2. **Python Script**:
   - Sends a request to the Arduino for the temperature.
   - Formats the temperature into a static prompt for a local LLM.
   - Sends the prompt to the **KoboldAI API** and retrieves a "weatherman-style" response.
   - Uses VoskAI for speech-to-text processing, listening for keywords to trigger temperature retrieval.
   - Converts the LLM output into speech using Pygame’s audio engine.
3. **Audio Output**: The AI-generated weather report is saved as an MP3 file and played aloud using Pygame.

## Software Dependencies

Ensure all dependencies are installed before running the project. The Python script requires:

- **pyserial** (For serial communication with Arduino)
- **vosk** (For speech-to-text processing)
- **pygame** (For text-to-speech output)
- **requests** (For interacting with the LLM API)
- **KoboldAI** (For hosting the local LLM)

To install them, run:

```bash
pip install pyserial vosk pygame requests dotenv
```

## Hardware Requirements

You'll need the following components:

- [Elegoo Arduino Mega 2560](https://www.elegoo.com/products/elegoo-mega-2560-r3)
- [AHT21 Temperature Sensor](https://www.adafruit.com/product/5180)
- USB Cable for Arduino Mega
- A computer capable of running a local LLM and Python scripts (I utilized a desktop for LLM processing, and a laptop for everything else)

## Setting Up KoboldAI

1. Download and install **KoboldAI** by following the instructions from [Kobold.cpp](https://github.com/LostRuins/koboldcpp).
2. Download a **GGUF model** suitable for your hardware. You can find models at [TheBloke's Hugging Face repository](https://huggingface.co/TheBloke) or similar sources.
3. Launch KoboldAI and load the selected model.
4. Ensure that the API mode is enabled so that the Python script can communicate with it.

## Setup & Installation

### Arduino Setup

1. Connect the AHT21 sensor to the Arduino Mega:

   - **VIN** → VIN
   - **GND** → GND
   - **SDA** → SDA (Pin 20)
   - **SCL** → SCL (Pin 21)

2. Upload the Arduino sketch (`arduino_script.ino`) using the **Arduino IDE**.

3. Open the serial monitor and confirm that the Arduino responds to requests by sending temperature data.

### Python Script Setup

1. Clone this repository:

```bash
git clone https://github.com/joeschmoe-dev/weather-ai.git
cd weather-ai
```

2. Set variables in the `.env` file, like `api-endpoint`


3. Run the Python script:

```bash
python listener.py
```

4. Speak the trigger phrase (e.g., "What's the weather / how hot is it / what should I wear") and listen as the AI generates and plays the weather report.

## Final Product

When the system is running:

- The microphone listens for keywords to trigger a weather update.
- The Arduino retrieves the temperature and sends it to the Python script via serial.
- The AI generates a weather report based on the current temperature.
- The report is converted to speech and played out loud.

## License

This project is covered under the [Together forever license](https://github.com/joeschmoe-dev/togetherforeverlicense)

