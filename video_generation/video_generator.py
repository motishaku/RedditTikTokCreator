import multiprocessing
import random
import os
from moviepy.video.tools.subtitles import TextClip
from textwrap import wrap
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.editor import ImageClip
from screenshots import SCREENSHOT_OUTPUT_FOLDER

END_OF_VIDEO_BUFFER = 7
INTERVAL_BETWEEN_TEXTS = 0.12
TITLE_PREVIEW_TIME = 2

GAMEPLAY_VIDEOS_PATH = os.path.join(os.getcwd(), "gameplays")


class VideoCreator:
    def __init__(self, clip_length, thread_id):
        self.output_path = os.path.join(os.getcwd(), "result", f"{thread_id}.mp4")
        self.thread_id = thread_id
        self.background_games = ["minecraft", "rocket_league", "gta", "steep", "multiversus", "fall_guys", "csgo",
                                 "cluster_truck"]
        self.gameplay_length = None
        self.clip_length = clip_length
        self.outro_length = None

        self.clips = []
        self.audios = []
        self.gameplay_file_name = self.choose_gameplay_video()
        self.video = self.load_video()
        self.clip_start, self.clip_end = self.set_clip_timestamps()
        self.width, self.height = self.calculate_phone_vid_size()
        self.crop_vid()
        self.latest_text_timestamp = 0

    def choose_gameplay_video(self):
        file_list = os.listdir(GAMEPLAY_VIDEOS_PATH)
        chosen_game = random.choice(self.background_games)
        game_videos = [file_name for file_name in file_list if chosen_game in file_name]
        return random.choice(game_videos)

    def set_clip_timestamps(self):
        clip_start = random.randrange(0, int(self.gameplay_length) - int(self.clip_length))
        clip_end = clip_start + self.clip_length + END_OF_VIDEO_BUFFER
        return clip_start, clip_end

    def load_video(self):
        vid_path = os.path.join(GAMEPLAY_VIDEOS_PATH, self.gameplay_file_name)
        vid = VideoFileClip(vid_path)
        self.gameplay_length = vid.duration
        return vid

    def crop_vid(self):
        vid = self.video.subclip(self.clip_start, self.clip_end)

        width, height = self.video.size
        crop_position = ((width - self.width) // 2, (height - self.height) // 2)
        vid = vid.crop(x1=crop_position[0],
                       y1=crop_position[1],
                       width=self.width,
                       height=self.height
                       )
        self.video = vid

    def calculate_phone_vid_size(self):
        width, height = self.video.size
        width = min(width, int(height * (9 / 16)))
        height = min(height, int(width * (16 / 9)))
        return width, height

    def place_credit(self):
        text_position = (
            self.width - 30,
            self.height - 30
        )
        credit = TextClip("@M", fontsize=13, font="Arial", color="white")
        text_clip = credit \
            .set_position(text_position) \
            .set_duration(self.video.duration) \
            .set_start(self.video.start)
        self.clips.append(text_clip)

    def place_title_screenshot_intro(self):
        screenshot_path = os.path.join(SCREENSHOT_OUTPUT_FOLDER, f"{self.thread_id}.jpg")
        image_clip = ImageClip(screenshot_path)

        image_position = (
            (self.width - image_clip.w) // 2,
            (self.height - image_clip.h) // 2 - 30
        )
        image_clip = image_clip.set_duration(TITLE_PREVIEW_TIME)\
            .set_start(self.video.start)\
            .set_position(image_position)
        self.clips.append(image_clip)

    def place_outro_image(self):
        image_clip = ImageClip("outro.png").resize(width=self.width, height=self.height)
        image_clip = image_clip.set_duration(2)\
            .set_start(self.latest_text_timestamp)
        self.clips.append(image_clip)

    def create_sentence_clip(self, tts_resource):
        text = tts_resource.text
        text_duration = tts_resource.length
        audio_file_path = tts_resource.file_path

        max_width = self.width - 55
        wrapped_text = "\n".join(
            wrap(text, width=int(max_width / 10)))  # Adjust the divisor (10) based on your font size

        text_clip = TextClip(wrapped_text, fontsize=24, font="Arial", color="white",
                             stroke_color="black", stroke_width=0.75)

        text_position = (
            (self.width - text_clip.w) // 2,
            (self.height - text_clip.h) // 2 - 30
        )

        text_clip = text_clip \
            .set_position(text_position) \
            .set_duration(text_duration) \
            .set_start(self.latest_text_timestamp)

        self.clips.append(text_clip)
        self.audios.append(
            AudioFileClip(audio_file_path)
            .set_duration(text_duration)
            .set_start(self.latest_text_timestamp)
        )

        print(f"[*] Created a clip from {self.latest_text_timestamp} to {self.latest_text_timestamp + text_duration}")

        self.latest_text_timestamp += text_duration + INTERVAL_BETWEEN_TEXTS

    def build_video_from_clips(self):
        self.video = CompositeVideoClip([self.video] + self.clips)
        self.video.audio = CompositeAudioClip(self.audios)

    def save_video(self):
        self.place_credit()
        self.place_outro_image()
        self.build_video_from_clips()
        self.video.write_videofile(
            self.output_path,
            audio_codec="aac",
            audio_bitrate="192k",
            threads=multiprocessing.cpu_count(),
            fps=24
        )
