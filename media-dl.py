import subprocess
import platform
import readline
import time
import glob
import sys
import os
import re

# =======================================================

print("Welcome to media-dl!")
print("")
if os.geteuid() == 0:
    pass
else:
    print("Please run as root!")
    exit
print("Checking Packages... ")
print("")
time.sleep(1.5)

try:
    import apt
    print("[√] Python Apt")
except ImportError as e:
    print("[x] Python Apt - Installing / Updating...")
    os.system("apt-get install --reinstall python3-apt >> /dev/zero 2>&1")
    import apt
    pass

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

cache = apt.Cache()
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
        open('/root/.media-dl', 'a').close()
        time.sleep(2)
    else:
        pass

title = f"""
{Fore.RED}                    _ _                  {Fore.LIGHTGREEN_EX}   _ _ 
{Fore.RED} _ __ ___   ___  __| (_) __ _            {Fore.LIGHTGREEN_EX}__| | | 
{Fore.RED}| '_ ` _ \ / _ \/ _` | |/ _` |{Fore.WHITE}  _____ {Fore.LIGHTGREEN_EX}  / _` | | {Fore.LIGHTBLUE_EX}GUI Version
{Fore.RED}| | | | | |  __/ (_| | | (_| |{Fore.WHITE} |_____|{Fore.LIGHTGREEN_EX} | (_| | |
{Fore.RED}|_| |_| |_|\___|\__,_|_|\__,_|         {Fore.LIGHTGREEN_EX} \__,_|_|                                        
"""

def path_completer(text, state): # https://stackoverflow.com/a/71332625
    line = readline.get_line_buffer().split()
    if '~' in text:
        text = os.path.expanduser('~')
    return([x for x in glob.glob(text+'*')][state])

def video_progress_bar(stream, chunk, bytes_remaining): # https://stackoverflow.com/a/68234125
    os.system("clear")
    print(title)
    #print(f"{Fore.LIGHTGREEN_EX}Downloading {Fore.LIGHTWHITE_EX}: {Fore.LIGHTRED_EX}" + download_vid.title)
    curr = stream.filesize - bytes_remaining
    done = int(50 * curr / stream.filesize)
    load = f'{Fore.LIGHTGREEN_EX}=' * done
    load1 = (' ' * (50-done))
    sys.stdout.write(f"\r{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX} {load} {load1} {Fore.LIGHTWHITE_EX}] ")
    sys.stdout.flush()
    print(f"{Fore.LIGHTRED_EX}" + download_vid.title)

def playlist_progress_bar(stream, chunk, bytes_remaining): # https://stackoverflow.com/a/68234125
    os.chdir(''+dir+'')
    os.system("clear")
    print(title)
    print(f'{Fore.LIGHTGREEN_EX}Downloading {Fore.WHITE}:{Fore.LIGHTRED_EX} ' + download_playlist.title)
    print(f'{Fore.LIGHTGREEN_EX}All Videos {Fore.WHITE}:{Fore.LIGHTRED_EX} %s ' % len(download_playlist.video_urls))
    print(f'{Fore.LIGHTGREEN_EX}Downloaded {Fore.WHITE}:{Fore.LIGHTRED_EX} ' + count)
    print(f'{Fore.LIGHTGREEN_EX}Errors {Fore.WHITE}:{Fore.LIGHTRED_EX} ' + str(errors))
    curr = stream.filesize - bytes_remaining
    done = int(50 * curr / stream.filesize)
    load = f'{Fore.LIGHTGREEN_EX}=' * done
    load1 = (' ' * (50-done))
    print("")
    sys.stdout.write(f"\r{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX} {load} {load1} {Fore.LIGHTWHITE_EX}] ")
    sys.stdout.flush()
    print(f"{Fore.LIGHTRED_EX}" + video.title)

check_valid_video = ("(https?://)?(www\.)?youtube\.(com|nl)/watch\?v=")
check_valid_playlist = ("(https?://)?(www\.)?youtube\.(com|nl)/playlist\?list=")
# =======================================================
os.system("clear")
print(title)
choices = TerminalMenu(["Download Youtube Video", "Download Youtube Playlist", "Download Tiktok Video", "Download Tiktok Channel", "Exit"])
choice_index = choices.show()

if choice_index == 0: # ---------------------------------------
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
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(path_completer)
    dir = input(f"{Fore.LIGHTGREEN_EX}Where is the file going to be downloaded? {Fore.WHITE}:{Fore.LIGHTGREEN_EX} {Fore.WHITE}")
    while os.path.isdir(dir) == False:
        print(f"{Fore.LIGHTRED_EX}Directory does not exist!")
        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(path_completer)
        dir = input(f"{Fore.LIGHTGREEN_EX}Where is the file going to be downloaded? {Fore.WHITE}:{Fore.LIGHTGREEN_EX} {Fore.WHITE}")
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
if choice_index == 1: # ---------------------------------------
    errors = 0
    playlist_url = input(f"{Fore.LIGHTGREEN_EX}Playlist Url {Fore.WHITE}: {Fore.LIGHTGREEN_EX}")
    check_playlist = re.compile(check_valid_playlist)
    while not re.search(check_playlist, playlist_url):
        if re.search(check_playlist, playlist_url):
            pass
        else:
            print(f"{Fore.LIGHTRED_EX}Playlist Url not valid!")
            playlist_url = input(f"{Fore.LIGHTGREEN_EX}Playlist Url {Fore.WHITE}: {Fore.LIGHTGREEN_EX}")
            re.search(check_playlist, playlist_url)
    print("")
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(path_completer)
    dir = input(f"{Fore.LIGHTGREEN_EX}Where is the file going to be downloaded? {Fore.WHITE}:{Fore.LIGHTGREEN_EX} {Fore.WHITE}")
    while os.path.isdir(dir) == False:
        print(f"{Fore.LIGHTRED_EX}Directory does not exist!")
        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(path_completer)
        dir = input(f"{Fore.LIGHTGREEN_EX}Where is the file going to be downloaded? {Fore.WHITE}:{Fore.LIGHTGREEN_EX} {Fore.WHITE}")
    print("")
    print(f"{Fore.LIGHTGREEN_EX}Choose download file format!")
    format = TerminalMenu(["Mp4", "Mp3"])
    format_index = format.show()
    download_playlist = Playlist(playlist_url)
    playlist_title_filter = re.sub('[^A-Za-z0-9]+','_', download_playlist.title)
    if format_index == 0:
        for video in download_playlist.videos:
            try:
                count = subprocess.getoutput('find -mindepth 1 -type f -name "*.mp4" -printf x | wc -c')
                video_title_filter = re.sub('[^A-Za-z0-9]+','_', video.title)
                video.register_on_progress_callback(playlist_progress_bar)
                video.streams.get_highest_resolution()
                video.streams.filter(adaptive=True, file_extension='mp4').first().download(filename='{}/{}.mp4'.format(dir,video_title_filter))
                video.register_on_progress_callback(playlist_progress_bar)
                video.streams.get_highest_resolution()
                video.streams.filter(only_audio=True, file_extension='webm').first().download(filename='{}/{}.mp3'.format(dir,video_title_filter))
                print(f"{Fore.LIGHTBLUE_EX}")
                os.system('ffmpeg -v quiet -stats -i '+dir+'/'+video_title_filter+'.mp4 -i '+dir+'/'+video_title_filter+'.mp3 -c:v copy -c:a aac '+dir+'/'+video_title_filter+'_ffmpeg.mp4')
                os.remove(''+dir+'/'+video_title_filter+'.mp3')
                os.remove(''+dir+'/'+video_title_filter+'.mp4')
                os.rename(''+dir+'/'+video_title_filter+'_ffmpeg.mp4', ''+dir+'/'+video_title_filter+'.mp4')
            except:
                errors + 1
                pass
        print("")
        print(f"{Fore.LIGHTGREEN_EX}Download Done!")
        print(f"{Fore.LIGHTBLUE_EX}Adding to zip file... {Fore.LIGHTRED_EX}This might take a while!")
        os.system('zip '+playlist_title_filter+'.zip *.mp4 >> /dev/zero')
        print(f"{Fore.LIGHTBLUE_EX}Removing Mp4 Files...")
        os.system("rm *.mp4")
        print("")
        print(f'{Fore.LIGHTGREEN_EX}File Path {Fore.WHITE}: {Fore.LIGHTRED_EX}'+dir+'/'+playlist_title_filter+'.zip')
    if format_index == 1:
        for video in download_playlist.videos:
            try:
                count = subprocess.getoutput('find -mindepth 1 -type f -name "*.mp3" -printf x | wc -c')
                video_title_filter = re.sub('[^A-Za-z0-9]+','_', video.title)
                video.register_on_progress_callback(playlist_progress_bar)
                video.streams.get_highest_resolution()
                video.streams.filter(only_audio=True, file_extension='webm').first().download(filename='{}/{}.mp3'.format(dir,video_title_filter))
            except:
                errors + 1
                pass
        print("")
        print(f"{Fore.LIGHTGREEN_EX}Download Done!")
        print(f"{Fore.LIGHTBLUE_EX}Making zip file... {Fore.LIGHTRED_EX}This might take a while!")
        os.system('zip '+playlist_title_filter+'.zip *.mp3 >> /dev/zero')
        print(f"{Fore.LIGHTBLUE_EX}Removing Mp3 Files...")
        os.system("rm *.mp3")
        print("")
        print(f'{Fore.LIGHTGREEN_EX}File Path {Fore.WHITE}: {Fore.LIGHTRED_EX}'+dir+'/'+playlist_title_filter+'.zip')
if choice_index == 2:
    print("third option")
if choice_index == 3:
    print("fourth option")
if choice_index == 4:
    print(f"{Fore.RESET}Goodbye!")
    exit()

print(f"{Fore.RESET}")

# DO NOT TOUCH THIS EMPTY LINE, IT WILL BREAK EVERYTHING!!!
