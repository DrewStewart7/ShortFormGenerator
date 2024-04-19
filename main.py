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

s = requests.session()

s.headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Sec-Ch-Ua":'"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Accept-Encoding":'gzip, deflate, br',
    "Referer":"https://savett.cc/en/",
    "Origin":"https://savett.cc",
    "Sec-Fetch-Site":"same-origin",
    "Sec-Fetch-User":'?1',
    "Authority":"savett.cc",
    "Path":"/en/download",
    "Cookie":'_ga=GA1.1.1398464719.1705359496; _cc_id=30bfb5fa79ac8e8c0b7639efda64e046; __qca=P0-741897807-1705359497254; _pbjs_userid_consent_data=3524755945110770; _sharedid=eff5a8af-5458-4f68-9d5e-b3dae5339896; _lr_env_src_ats=false; cookie=e8794a4a-fda0-4ec9-b5bd-8a64ce554ff1; cookie_cst=zix7LPQsHA%3D%3D; fs.admiral.whitelisted=true; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3AVUdkXS5niDK_TGCxkkaLldlrw9kQB7_k9KCwrjTPL3v1FNkGHdcOvvsyU-odz03P_ba1aq2uEsVIX4XMAOHRhN-slkIayFQQwb9WIZlp1NTWXUwTIn4NCoJLmm5QQ-_J%22%7D; panoramaId_expiry=1706570562034; panoramaId=48ec1c3b7c7cd845ca7864c4041a4945a7023439f911a257412801226684a8c0; panoramaIdType=panoIndiv; cf_clearance=uIhEWO9jLDME9XAD6q04Ri1PyPRid3TsP16mZ1VY5_g-1706053707-1-AdZILqYu4/vL6WarsL51238IdMVvt+tVIWv1f/uREVtszuyBujuy15qR6NBbwtnfPV2VCO7HR6J0B43KwRbuEZM=; _lr_sampling_rate=100; session=eyJjc3JmX3Rva2VuIjoiYTVjMGRlM2U3YThmYjRkZGMzZDIxNzMyYzIxMDRmOGM4NDVhYzg0YiJ9.GJILYA.F0fTGMgTwAVjaX2nIxLX14RtcF8; pbjs_fabrickId_cst=zix7LPQsHA%3D%3D; _lr_retry_request=true; __gads=ID=4ba222ca108651ca:T=1705359498:RT=1706072350:S=ALNI_MasQJ8vgWaF5X7sTdYfikzzv29Qxg; __gpi=UID=00000d63ecf8393a:T=1705359498:RT=1706072350:S=ALNI_MY5afMVmsqHfVNpvUbmp0zKLJC1pQ; _ga_96M898LV38=GS1.1.1706071187.13.1.1706072363.0.0.0; cto_bundle=lLRaU185ZjN2T3JibHNoZHR1UjAzTzBNU2xoOTFicDd0JTJGV2hObm9TWU9RYkp5U0Ixc1Jhdkk3TndlVnBFVjZGZXN1RGNNUFNSczBuNkxQJTJGaU5WeW1oeGVMY1hTcGlVMU5UdXFkU3BRb0JFQzR4eGpYZjFvdER4TGtZZzNtRFpnNSUyQjJzOWpJMDJWdVlsem5NdmYlMkJRUVBnJTJGc0hWUk8lMkJPU0hNa1l6djJQSGVsVDViM3JFViUyQlBrOTRPV0FBJTJCNGI5Uk9EYUhUMEVnN2lVSHF2NmVKbTlwMDh2aGNtcTFQS2VuZ2JIczl1NEdEOVAxcDl5SzJEZnRjM1dUM1paM2QlMkZMVHBHMFZv; cto_bidid=6gpktV82SkFRUjRqMHJWdW5naXd0Z29JQlRSMXhsSU9JODVRR0lCVmU1JTJGSTJFdGVZVDdoUTJTQVhHdjFRSm9ndERkUSUyQkRjQ01iZnJxalVOUmMzcnVPb1kweGpJbDA3d0VoUjNsZ3NNOG16TUZEd3MlM0Q; _awl=2.1706072364.5-9e0f8c241ebae52df1c7cc4ed060c4f5-6763652d75732d63656e7472616c31-7'
}
csrfreq = s.get("https://savett.cc/en/")
csrf = csrfreq.text.split('csrf_token" value=')[1].split('"')[1]


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

        # Write the result to a file
        final_clip.write_videofile(f"{cwd}\outputs\{caption}.mp4", codec="libx264", threads=10)
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
