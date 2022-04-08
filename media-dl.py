import platform
import time
import sys
import apt
import os
import re

# =======================================================

print("Welcome to media-dl!")
print("")
print("Checking Packages... ")
print("")
time.sleep(1.5)
cache = apt.Cache()

try:
    from colorama import Fore
    print("[√] Colorama")
except ImportError as e:
    print("[x] Colorama - Installing / Updating...")
    os.system("pip install colorama >> /dev/zero")
    from colorama import Fore
    pass

try:
    from pytube import *
    print("[√] Pytube")
except ImportError as e:
    print("[x] Pytube - Installing / Updating...")
    os.system("pip install pytube >> /dev/zero")
    from pytube import *
    pass

try:
    from simple_term_menu import TerminalMenu
    print("[√] Simple Term Menu")
except ImportError as e:
    print("[x] Simple Term Menu - Installing / Updating...")
    os.system("pip install simple_term_menu >> /dev/zero")
    from simple_term_menu import TerminalMenu
    pass

if 'ffmpeg' in cache:
    package_installed = cache['ffmpeg'].is_installed
    if package_installed == False:
        print("[x] Ffmpeg - Installing / Updating...")
        os.system("apt-get install ffmpeg -y >> /dev/zero 2>&1")
    else:
        print("[√] Ffmpeg")

print("")

if platform.system() == "Linux" or platform.system() == "win":
    print(f"{Fore.YELLOW}Suported OS ( {Fore.RED}%s {Fore.YELLOW}) detected..." % platform.system())

if platform.system() == "Linux":
    if os.path.isfile('/root/.media-dl') == False:
        print(f"{Fore.LIGHTMAGENTA_EX}First time run detected. Thanks for using my software! :)")
        print("")
        time.sleep(1)
    else:
        pass

title = f"""
{Fore.RED}                    _ _                  {Fore.LIGHTGREEN_EX}   _ _ 
{Fore.RED} _ __ ___   ___  __| (_) __ _            {Fore.LIGHTGREEN_EX}__| | | 
{Fore.RED}| '_ ` _ \ / _ \/ _` | |/ _` |{Fore.WHITE}  _____ {Fore.LIGHTGREEN_EX}  / _` | | {Fore.LIGHTBLUE_EX}GUI Version
{Fore.RED}| | | | | |  __/ (_| | | (_| |{Fore.WHITE} |_____|{Fore.LIGHTGREEN_EX} | (_| | |
{Fore.RED}|_| |_| |_|\___|\__,_|_|\__,_|         {Fore.LIGHTGREEN_EX} \__,_|_|                                        
"""
def video_progress_bar(stream, chunk, bytes_remaining): # https://stackoverflow.com/questions/49185538/how-to-add-progress-bar
    os.system("clear")
    print(title)
    #print(f"{Fore.LIGHTGREEN_EX}Downloading {Fore.LIGHTWHITE_EX}: {Fore.LIGHTRED_EX}" + download_vid.title)
    curr = stream.filesize - bytes_remaining
    done = int(50 * curr / stream.filesize)
    load = '\033[32m=' * done
    load1 = (' ' * (50-done))
    sys.stdout.write(f"\r{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX} {load} {load1} {Fore.LIGHTWHITE_EX}] ")
    sys.stdout.flush()
    print(f"{Fore.LIGHTRED_EX}" + download_vid.title)

check_valid_video = ("(https?://)?(www\.)?youtube\.(com|nl)/watch\?v=([-\w]+)")

# =======================================================
os.system("clear")
print(title)
choices = TerminalMenu(["Download Youtube Video", "Download Tiktok Video", "Download Youtube Playlist", "Download Tiktok Channel", "Merge All Videos In Folder", "Exit"])
choice_index = choices.show()

if choice_index == 0:
    video_url = input(f"{Fore.LIGHTGREEN_EX}Video Url {Fore.WHITE}: {Fore.LIGHTGREEN_EX}")
    check_video = re.compile(check_valid_video)
    while not re.search(check_video, video_url):
        if re.search(check_video, video_url):
            pass
        else:
            print(f"{Fore.LIGHTRED_EX}Video Url not valid!")
            video_url = input(f"{Fore.LIGHTGREEN_EX}Video Url {Fore.WHITE}: {Fore.LIGHTGREEN_EX}")
            re.search(check_video, video_url)
    print("")
    dir = input(f"{Fore.LIGHTGREEN_EX}Where is the file going to be downloaded? {Fore.WHITE}:{Fore.LIGHTGREEN_EX} ")
    while os.path.isdir(dir) == False:
        print(f"{Fore.LIGHTRED_EX}Directory does not exist!")
        dir = input(f"{Fore.LIGHTGREEN_EX}Where is the file going to be downloaded? {Fore.WHITE}:{Fore.LIGHTGREEN_EX} ")
    print("")
    print(f"{Fore.LIGHTGREEN_EX}Choose download file format!")
    format = TerminalMenu(["Mp4", "Mp3"])
    format_index = format.show()
    if format_index == 0:
        download_vid = YouTube(video_url, on_progress_callback=video_progress_bar)
        video_title_filter = re.sub('[^A-Za-z0-9]+','_', download_vid.title)
        download_vid = YouTube(video_url, on_progress_callback=video_progress_bar)
        download_vid.register_on_progress_callback(video_progress_bar)
        download_vid.streams.get_highest_resolution()
        download_vid.streams.filter(adaptive=True, file_extension='mp4').first().download(filename='{}/{}.mp4'.format(dir,video_title_filter))
        download_vid.streams.get_highest_resolution()
        download_vid.streams.filter(only_audio=True, file_extension='webm').first().download(filename='{}/{}.mp3'.format(dir,video_title_filter))
        print(f"{Fore.LIGHTBLUE_EX}")
        os.system('ffmpeg -v quiet -stats -i '+dir+'/'+video_title_filter+'.mp4 -i '+dir+'/'+video_title_filter+'.mp3 -c:v copy -c:a aac '+dir+'/'+video_title_filter+'_ffmpeg.mp4')
        os.remove(''+dir+'/'+video_title_filter+'.mp3')
        os.remove(''+dir+'/'+video_title_filter+'.mp4')
        os.rename(''+dir+'/'+video_title_filter+'_ffmpeg.mp4', ''+dir+'/'+video_title_filter+'.mp4')
        print(f'{Fore.LIGHTGREEN_EX}File Path {Fore.WHITE}: {Fore.LIGHTRED_EX}'+dir+'/'+video_title_filter+'.mp4')
    if format_index == 1:
        download_vid = YouTube(video_url, on_progress_callback=video_progress_bar)
        video_title_filter = re.sub('[^A-Za-z0-9]+','_', download_vid.title)
        download_vid = YouTube(video_url, on_progress_callback=video_progress_bar)
        download_vid.register_on_progress_callback(video_progress_bar)
        download_vid.streams.get_highest_resolution()
        download_vid.streams.filter(only_audio=True, file_extension='webm').first().download(filename='{}/{}.mp3'.format(dir,video_title_filter))
        print(f"{Fore.LIGHTBLUE_EX}")
        print(f'{Fore.LIGHTGREEN_EX}File Path {Fore.WHITE}: {Fore.LIGHTRED_EX}'+dir+'/'+video_title_filter+'.mp4')
if choice_index == 1:
    print("second option")
if choice_index == 2:
    print("third option")
if choice_index == 3:
    print("fourth option")
if choice_index == 4:
    print("fifth option")
if choice_index == 5:
    print(f"{Fore.RESET}Goodbye!")
    exit

print(f"{Fore.RESET}")
