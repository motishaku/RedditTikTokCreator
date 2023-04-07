from cleanup_utils import cleanup_tts_samples
from reddit import RedditConnector
from screenshots import ScreenshotManager
from tts import TikTok_TTS
from video_generation import VideoCreator

r = RedditConnector()
r.login()
r.get_subreddit()
r.get_thread()
thread = r.chosen_thread

sentences = r.get_thread_text()
voices = []
clip_length = 0


if thread.selftext:
    text = r.chosen_thread.title
    sentences.insert(0, text)
else:
    # ScreenshotManager(thread.id, thread.url).take_screenshot()
    # vid.place_title_screenshot_intro()
    pass

for sentence in sentences:
    tts = TikTok_TTS(sentence)
    tts.generate_voice()
    clip_length += tts.length
    voices.append(tts)

vid = VideoCreator(clip_length=clip_length, thread_id=thread.id)

for v in voices:
    vid.create_sentence_clip(v)

vid.save_video()
r.set_thread_as_used(thread.id)
cleanup_tts_samples()