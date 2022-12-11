import whisper


def transcribe(input_file):
    """Accepts an audio file.
    Returns a text of the audio file"""
    model = whisper.load_model("tiny")
    result = model.transcribe(input_file)
    return result["text"]
