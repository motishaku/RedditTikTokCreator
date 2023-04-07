import io

from tts import Voice
from tts.consts import TIKTOK_USER_AGENT, TIKTOK_API_URL
import os
import requests
import base64
import uuid
from pydub import AudioSegment


class TikTok_TTS:
    def __init__(self, text):
        self.voice = Voice.EN_US_001.value
        self.length = None
        self.default_path = os.path.join(os.getcwd(), "tts_samples")
        self.text = text
        self.tiktok_session_id = ""
        self.file_name = self._generate_file_name()
        self.file_path = os.path.join(self.default_path, self.file_name)

    def _generate_file_name(self):
        files = os.listdir(self.default_path)
        while True:
            file_name = str(uuid.uuid4()).replace("-", '')
            if file_name not in files:
                return f"{file_name}.mp3"

    def text_clean_up(self):
        """
        Cleaning up text from banned words because of some
        :return:
        """

    def generate_voice(self):
        self.text = self.text.replace("+", "plus")
        self.text = self.text.replace("&", "and")
        params = {"req_text": self. text, "speaker_map_type": 0, "aid": 1233, "text_speaker": self.voice}
        headers = {
            "User-Agent": TIKTOK_USER_AGENT,
            "Cookie": f"sessionid={self.tiktok_session_id}"
        }
        r = requests.post(TIKTOK_API_URL, headers=headers, params=params)
        if r.json()["message"] == "Couldn't load speech. Try again.":
            output_data = {"status": "Session ID is invalid", "status_code": 5}
            print(output_data)
            return output_data

        vstr = r.json()["data"]["v_str"]

        b64d = base64.b64decode(vstr)
        with open(self.file_path, "wb") as out:
            out.write(b64d)

        audio_buffer = io.BytesIO(b64d)
        audio = AudioSegment.from_file(audio_buffer, format="mp3")
        self.length = len(audio) / 1000