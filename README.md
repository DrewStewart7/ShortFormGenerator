```python main.py``` to run


**QUICK FIX**
Also run `python -m playwright install` in command prompt please

# ShortFormGenerator
Capable of assembling **hundreds** of videos per day.
Generates short form videos (1080x1920, < 60s) using content from TikTok. Adds a subclip and background to create "unique" content. 
**Please do not post the generated content anywhere, as it belongs to it's original TikTok creator**.
I created this program for fun, and to learn new skills such as movie.py and working with downloading files from the internet.
It was a nice little challenge.

**Here is an example output**
https://youtube.com/shorts/IJi9FgQAovs

# How it works
1. Selects a random topic from the list of topics the user creates
2. Searches for videos with the topic as a hashtag on TikTok
3. Selects a random video with that hashtag
4. Uses a 3rd party API (no API key needed) to download the video without a watermark
5. Combines the TikTok video, a secondary video, and a background image together into one video
6. Saves the result into the outputs folder
7. Repeats indefinitely until the user ends the program

# Setup Instructions

Follow the youtube video instructions below. I've made an update since that YT video was created though. The update introduces
the options screen. The options include:
1 Download videos from tiktok (original version)
2 Use videos from 'feed' folder - uses these videos instead of ones from TikTok
3 Split one video in 'feed' into smaller parts - splits one large video into smaller parts (user chooses length in seconds), edits, and saves them seperately

As you can see from the options, your 'input' videos will go into the 'feed' folder and the output will be saved into the 'outputs' folder.

https://www.youtube.com/watch?v=BHc_72r4yzM&ab_channel=DeveloperDrew

# Special Thanks to akasakaid, aka Fawwaz Thoerif
Their TiktokDownloader repo has been helpful to download tiktok videos without a watermark. I used and modified 
a couple python files from https://github.com/akasakaid/TiktokDownloader

Thank you again, Fawwaz!


