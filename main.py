# Created by Drew Stewart January 2024
# Current version date: 5/17/24

#import required modules
import requests,json,time,os, asyncio, random, multiprocessing,colorama
from tiktok_downloader import downloader
from TikTokApi import TikTokApi
from moviepy.editor import VideoFileClip, clips_array, ImageClip, CompositeVideoClip, vfx
colorama.init(autoreset=True)
from colorama import Fore, Back, Style
cwd = os.getcwd()

#set up program to work with values in config
config = {}
with open(f'{cwd}\config.json','r') as file:
    config = json.loads(file.read())
topics = config["topics"]
print("Using topics:",topics)
ms_token = config["ms-token"]
if config["ms-token"] != None:
    print("Got MS-Token from config")
secondary_vid = config["secondary_video"]
print("Using secondary video:",secondary_vid)

#define static request urls
downUrl = "https://savett.cc/en/download"
mainurl = "https://savett.cc/en/"
newdurl = "https://dl2.savett.cc/file/"
trigurl = 'https://savett.cc/en/trigger-download'

#define downloader object
dl = downloader("video.mp4")




#try different sites to download the tiktok video from
def tryDownload(text):
    res = dl.tiktapio(text)
    if res:
        print("[+] success download with tiktapio !")
        
        return

    res = dl.tiktapiocom(text)
    if res:
        print("[+] success download with tiktapiocom !")
       
        return

    res = dl.tikmatecc(text)
    if res:
        print("[+] success download with tikmatecc !")
        
        return

    res = dl.snaptikpro(text)
    if res:
        print("[+] success download with snaptikpro !")
       
        return

    res = dl.musicaldown(text)
    if res:
        print("[+] success download with musicaldown !")
        return
    
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def editLongVideo(path, clip_length):
    print('\nEditing video...')
    # Load videos
    clip1 = VideoFileClip(path)
    clip2 = VideoFileClip(secondary_vid)

    # Remove sound from clip2
    clip2 = clip2.without_audio()

    # Calculate the number of clips
    num_clips = int(clip1.duration // clip_length)

    for i in range(num_clips):
        start_time = i * clip_length
        end_time = (i + 1) * clip_length

        # Process each clip
        processClip(clip1, clip2, start_time, end_time, i, path)

    # Handle the remaining seconds
    if clip1.duration % clip_length > 0:
        start_time = num_clips * clip_length
        end_time = clip1.duration  # till the end of the video

        # Process the last clip
        processClip(clip1, clip2, start_time, end_time, num_clips, path)

def processClip(clip1, clip2, start_time, end_time, i, path):
    # Trim clip1 and clip2
    clip1_sub = clip1.subclip(start_time, end_time)
    clip2_sub = clip2.subclip(start_time, end_time)

    # Resize videos
    # Assuming the final video size is 1090x1920
    clip1_resized = clip1_sub.resize(height=1920 * 2/3) # Top 2/3
    clip2_resized = clip2_sub.resize(height=1920 * 1/3) # Bottom 1/3

    # Load the background image
    bg_image = ImageClip("background.png").set_duration(clip1_sub.duration)

    # Resize the background image to the desired size
    bg_image = bg_image.resize(newsize=(1080, 1920))

    # Overlay the video clips on the background image
    final_clip = CompositeVideoClip([bg_image, clip1_resized.set_position(("center", "top")), clip2_resized.set_position(("center", "bottom"))])
    
    filename = path.split('\\')[-1].split('.')[0]
    caption = f"{filename}_{i}"
    final_clip.write_videofile(f"{cwd}\\outputs\\{caption}.mp4", codec="libx264", threads=16)
    print(Fore.GREEN + f"\nVideo editing finished - Saved at {cwd}\\outputs\\{caption}.mp4\n")

def editVideo(path):
    print('\nEditing video...')
    # Load videos
    clip1 = VideoFileClip(path)
    clip2 = VideoFileClip(secondary_vid)

    # Remove sound from clip2
    clip2 = clip2.without_audio()

    randstart = random.randint(0,int(clip2.duration-clip1.duration))

    # Trim clip2 to the duration of clip1
    clip2 = clip2.subclip(randstart, randstart + clip1.duration)

    # Resize videos
    # Assuming the final video size is 1090x1920
    clip1_resized = clip1.resize(height=1920 * 2/3) # Top 2/3
    clip2_resized = clip2.resize(height=1920 * 1/3) # Bottom 1/3

    # Load the background image
    bg_image = ImageClip("background.png").set_duration(clip1.duration)

    # Resize the background image to the desired size
    bg_image = bg_image.resize(newsize=(1080, 1920))

    # Overlay the video clips on the background image
    final_clip = CompositeVideoClip([bg_image, clip1_resized.set_position(("center", "top")), clip2_resized.set_position(("center", "bottom"))])
    
    caption = path.split("\\")[-1].split(".")[0]
    final_clip.write_videofile(f"{cwd}\outputs\{caption}.mp4", codec="libx264", threads=16)
    path = f"{cwd}\outputs\{caption}.mp4"
    print(Fore.GREEN + f"\nVideo editing finished - Saved at {path}\n")

#download video at the url selected by find_video
def downloadVid(url,caption,username):
    try:
        dl.setName(f"{cwd}\downloads\{caption}.mp4")

        tryDownload(url)

        print('\nEditing video...')
        # Load videos
        clip1 = VideoFileClip(f"{cwd}\downloads\{caption}.mp4")
        clip2 = VideoFileClip(secondary_vid)

        # Remove sound from clip2
        clip2 = clip2.without_audio()

        randstart = random.randint(0,int(clip2.duration-clip1.duration))

        # Trim clip2 to the duration of clip1
        clip2 = clip2.subclip(randstart, randstart + clip1.duration)

        # Resize videos
        # Assuming the final video size is 1090x1920
        clip1_resized = clip1.resize(height=1920 * 2/3) # Top 2/3
        clip2_resized = clip2.resize(height=1920 * 1/3) # Bottom 1/3

        # Load the background image
        bg_image = ImageClip("background.png").set_duration(clip1.duration)

        # Resize the background image to the desired size
        bg_image = bg_image.resize(newsize=(1080, 1920))

        # Overlay the video clips on the background image
        final_clip = CompositeVideoClip([bg_image, clip1_resized.set_position(("center", "top")), clip2_resized.set_position(("center", "bottom"))])
        
        
        final_clip.write_videofile(f"{cwd}\outputs\{caption}.mp4", codec="libx264", threads=16)
        path = f"{cwd}\outputs\{caption}.mp4"
        print(Fore.GREEN + f"\nVideo editing finished - Saved at {path}\n")
        #uploadVid(path,username,caption)
    except Exception as E:
        print(E)
        return None

#search tiktok for a video using the randomly selected hashtag
async def find_video(term):
    random.seed
    print('Finding video with topic:',term)
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3,headless=False)
        hashtag = api.hashtag(name=term)
        videos = []
        async for video in hashtag.videos(count=200):
            try: 
                info = video.as_dict
                dur = info['music']['duration']
                caption = info['contents'][0]['desc']
                if int(dur) <= 120 and not 'Reply to' in caption and not '@' in caption and not 'shop' in caption:
                    videos.append(video)
            except:
                api.close_sessions()
                find_video(term)
        api.close_sessions()
        try:
            video = videos[random.randint(0,len(videos)-1)]
            info = video.as_dict
            username = info['author']['uniqueId']
            caption = info['contents'][0]['desc']
            id = info['id']
            dur = info['music']['duration']
            link = f'https://www.tiktok.com/@{username}/video/{id}'
            print(Fore.YELLOW + '\nFound video')
            print('\nTopic:',term)
            print('Username:',username)
            print('Caption:', caption)
            print('Link:',link)
            print('Duration in seconds:', dur)
            print('\nDownloading video without watermark... This might take a minute...')
            downloadVid(link,caption,username)
        except:
            find_video(term)
        
def main():        
    #main event loop
    print("\nOptions\n\n1 Download videos from tiktok\n2 Use videos from 'feed' folder\n3 Split one video in 'feed' into smaller parts")
    choice = input("\nPlease enter your choice (ex: 1): ")
    if choice == '1':
        print("Downloading videos from tiktok...")
        while True:
            try:
                #get the topic
                random.seed
                term = topics[random.randint(0,(len(topics)-1))]
                
                
                
                asyncio.run(find_video(term))
                
                #tiktokl = input("Please enter the tiktok video link: ")
            except Exception as e:
                print(e)
                print("Error, restarting...")
                continue
    elif choice == '2':
        print("Using videos from 'feed' folder")
        for file in os.listdir(f"{cwd}\\feed"):
            print(f"Processing {file}")
            editVideo(f"{cwd}\\feed\{file}")
    elif choice == '3':
        print("Splitting one video in 'feed' into smaller parts")
        vname = input("\nWhat is the video name, including the extension? (ex: video.mp4) ")
        length = input("\nHow long should each clip be in seconds? (ex: 30) ")
        length = int(length)
        path = f"{cwd}\\feed\{vname}"
        
        print(f"Processing {vname}")
        editLongVideo(path, length)
    else:
        print("Invalid choice, please try again")
        main()
if __name__ == "__main__": 
    main()

    #multiprocessing, if you'd like to use it
    """ # creating processes
    processes = [multiprocessing.Process(target=main, args=()) for _ in range(1)]

    # starting processes
    for process in processes:
        process.start()
        time.sleep(3)

    # wait until all processes are finished
    for process in processes:
        process.join()
  
    # both processes finished 
    print("Done!")  """
