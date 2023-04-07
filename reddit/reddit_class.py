from reddit.consts import USER_AGENT
import praw
from prawcore.exceptions import OAuthException
import random
import nltk
import os

REDDIT_USED_THREADS_PATH = os.path.join(os.getcwd(), "reddit_used_vids.txt")


class RedditConnector:
    def __init__(self):
        self.chosen_thread = None
        self.read_post = None
        self.thread_minimum_comments = 25
        self.subreddit = None
        self.subreddits = ["AmItheAsshole"]
        self.username = None
        self.password = None
        self.client_id = None
        self.client_secret = None
        self.connection = None
        self.connected = None

    def login(self):
        try:
            self.connection = praw.Reddit(
            )
            self.validate_connection()
            self.connected = True
        except OAuthException:
            print("[*] Invalid credentials.")

    def validate_connection(self):
        self.connection.user.me()

    def _choose_random_subreddit(self):
        return random.choice(self.subreddits).strip()

    def get_subreddit(self):
        sub_name = self._choose_random_subreddit()
        subreddit = self.connection.subreddit(sub_name)
        self.subreddit = subreddit

    @staticmethod
    def _thread_was_used(thread_id):
        with open(REDDIT_USED_THREADS_PATH, 'r') as f:
            data = f.read()
            if thread_id in data:
                return True

    @staticmethod
    def set_thread_as_used(thread_id):
        with open(REDDIT_USED_THREADS_PATH, 'a') as f:
            f.writelines(thread_id + "\n")

    def get_thread(self):
        for thread in self.subreddit.hot(limit=25):
            if self._thread_was_used(thread.id):
                print(f"[*] Thread id {thread.id} is already used, skipping")
                continue
            if thread.over_18:
                print(f"[*] Thread id {thread.id} is NSFW, skipping")
                continue
            if not thread.selftext:
                print(f"[*] Thread id {thread.id} is not currently supporting threads with no text, skipping")
                continue
            if thread.stickied:
                print(f"[*] Thread id {thread.id} is pinned, skipping")
                continue
            if self.read_post and not thread.is_self:
                print(f"[*] Thread id {thread.id} is not a post thread")
                continue
            if self.thread_minimum_comments > thread.num_comments and not self.read_post:
                print(f"[*] Thread id {thread.id} does not have enough comments, thread has {thread.num_comments} but "
                      f"the set limit is {self.thread_minimum_comments}, skipping")
                continue

            self.chosen_thread = thread
            break
        else:
            print("[*] All threads in hot section are used")

    def get_thread_stats(self):
        return {
            "upvote_ratio": self.chosen_thread.upvote_ratio,
            "upvotes": self.chosen_thread.score,
            "rewards": len(self.chosen_thread.all_awardings),
            "comments": self.chosen_thread.num_comments
        }

    def get_thread_text(self):
        text = self.chosen_thread.selftext
        sentences = nltk.sent_tokenize(text)
        return sentences


