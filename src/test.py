from TTS.api import TTS

# Initialize TTS with a pre-trained model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA", gpu=False)

# Generate speech with custom settings
tts.tts_to_file(
    text="Hello, this is Coqui TTS speaking!",
    file_path="output.wav",
    speaker_idx=0,  # Choose a speaker (if model supports multi-speaker)
    speed=1.0,      # Adjust speaking speed (default is 1.0)
    emotion="neutral"  # Some models support emotional tones
)
