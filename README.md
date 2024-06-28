# David Attenborough Narrates Your Life

This project was inspired by [cbh123/narrator](https://github.com/cbh123/narrator).

## Features

- **Live Camera Capture:** Continuously captures frames from your webcam
- **Narration:** Generates and plays audio narration for the captured frames in the style of Sir David Attenborough

## Setup

1. **Clone the repository** and set up a virtual environment:

    ```bash
    git clone <repository-url>
    cd narrator
    pip install virtualenv
    virtualenv narrator
    narrator\Scripts\activate  # On Windows
    source narrator/bin/activate  # On MacOS/Linux
    ```

2. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Create accounts and set up your API keys**:

    - Create an [OpenAI](https://platform.openai.com/docs/overview) account.
    - Create an [ElevenLabs](https://elevenlabs.io) account.

4. **Set your API keys** in a new `.env` file in the root directory:

    ```plaintext
    OPENAI_API_KEY='your_openai_api_key'
    ELEVENLABS_API_KEY='your_elevenlabs_api_key'
    ELEVENLABS_VOICE_ID='your_elevenlabs_voice_id'
    ```

5. **Obtain a voice ID from ElevenLabs**:

    - Create a new voice in ElevenLabs.
    - Get the voice ID using their [Get Voices API](https://elevenlabs.io/docs/api-reference/voices) or by clicking the flask icon next to the voice in the VoiceLab tab.
    - Add the voice ID to the `.env` file.

    Please ensure that you only use voices for which you have the legal rights and permissions. Unauthorized use of voices may infringe on intellectual property rights and privacy laws.

## Running the Project

Run the main script in the terminal:

```bash
python app.py
```

## Tips
- **Custom Image Narration**: If you prefer not to use the capture camera code, you can replace the `frame.jpg` image in the `./frames/` directory with an image of your choice. When you start the narration, the program will narrate the image you placed there instead.
