import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver.common.by import By

SCREENSHOT_OUTPUT_FOLDER = os.path.join(os.getcwd(), "screenshots", "assets")


class ScreenshotManager:
    def __init__(self, thread_id, thread_url):
        self.thread_id = thread_id
        self.thread_url = thread_url
        self.output_path = os.path.join(SCREENSHOT_OUTPUT_FOLDER, f"{thread_id}.jpg")

    def take_screenshot(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--window-size=1200x600')

        driver = webdriver.Chrome(options=options)
        driver.get(self.thread_url)

        title_element = driver.find_element(By.ID, f't3_{self.thread_id}')
        location = title_element.location
        size = title_element.size

        driver.save_screenshot('temp_screenshot.png')

        driver.quit()

        x, y, width, height = location['x'], location['y'], size['width'], size['height']
        im = Image.open('temp_screenshot.png')
        im = im.crop((x, y, x + width, y + height))
        im = im.convert("RGB")
        im.save(self.output_path)

        os.remove('temp_screenshot.png')

    def cleanup(self):
        files_list = [f for f in os.listdir(SCREENSHOT_OUTPUT_FOLDER) if not os.path.isdir(f)]
        for file in files_list:
            os.remove(os.path.join(SCREENSHOT_OUTPUT_FOLDER, file))
