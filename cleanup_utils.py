import os

tts_sample_path = os.path.join(os.getcwd(), "tts_samples")


def cleanup_tts_samples():
    try:
        for file in os.listdir(tts_sample_path):
            os.remove(os.path.join(tts_sample_path, file))
    except FileNotFoundError:
        pass
