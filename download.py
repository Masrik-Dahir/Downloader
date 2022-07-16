import datetime
import logging
import youtube_dl
import sys
from pytube import YouTube
import requests
from bs4 import BeautifulSoup
import custom
from moviepy.video.io.VideoFileClip import VideoFileClip

videos = [".mkv", ".webm", ".flv", ".vob", ".ogv", ".ogg", ".drc",
          ".gif", ".gifv", ".mng", ".avi", ".MTS", ".M2TS", ".TS"
          ".qt", ".mov", ".wmv", ".yuv", ".rm", ".rmvb", ".viv",
          ".asf", ".amv", ".mp4", ".m4p", ".m4v", ".mpg", ".mp2",
          ".mpeg", ".mpe", ".mpv", ".mpg", ".mpeg", ".m2v", ".m4v",
          ".svi", ".3gp", ".3g2", ".mxf", ".roq", ".nsv", ".flv",
          ".f4v", ".f4p", ".f4a", ".f4b", ".idx", ".sub"]

class TeeLogger(object):
    def debug(self, msg):
        logging.debug(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

def get_a(archive_url):
    r = requests.get(archive_url)
    soup = BeautifulSoup(r.content, "html.parser")
    links = soup.findAll('a')
    result = []
    baselink = archive_url.split('/')[0:3]
    baselink = baselink[0] + '//' + baselink[2]

    for link in links:
        absolute_link = link.get('href')
        if not str(link.get('href')).startswith('http'):
            absolute_link = baselink + str(link.get('href'))
        for extention in videos:
            if extention in absolute_link:
                result.append(absolute_link)
    custom.C_list(result).remove_duplicate()
    return result

def download_video_series(video_links, loc):
    for link in video_links:
        file_name = loc + list(''.join(link.split('/')[1:]).split('.' + link.split('.')[-1].split('?')[0]))[0] + '.' + link.split('.')[-1].split('?')[0]
        r = requests.get(link, stream=True)
        try:
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print("Finished Download --> %s" % file_name)
        except:
            None

    return "Done"

def youtube(link):
    try:
        yt = YouTube(link)
        ys = yt.streams.get_highest_resolution()
        ys.download()
        print("Finished Downloaded --> " + str(ys.default_filename))
        return True
    except:
        return False

def video(archive_url, loc):
    try:
        video_links = get_a(archive_url)
        download_video_series(video_links, loc)
        return "Downloaded --> {}".format(archive_url)
    except:
        return ""

def ph_alive_check(url):
    requested = requests.get(url)
    if requested.status_code == 200:
        print("and the URL is existing.")
    else:
        print("but the URL does not exist.")
        sys.exit()

def custom_dl_download(url, loc):
    ph_alive_check(url)

    outtmpl = loc + '%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'best',
        'outtmpl': outtmpl,
        'nooverwrites': True,
        'no_warnings': False,
        'ignoreerrors': True,
        'logger': TeeLogger(),
        'writedescription': True,
        'quiet': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        logging.basicConfig(filename='Log/Log {}.log'.format(str(datetime.datetime.now()).replace(':', '-')), level=logging.NOTSET, format='')
        try:
            ydl.download([url])
        except:
            logging.exception('')
            raise

    return "Downloaded --> {}".format(url)

def main(url, loc=''):
    # youtube(url)
    custom_dl_download(url, loc)
    video(url, loc)

def mp4tomp3(mp4file, mp3file):
    videoclip = VideoFileClip(mp4file)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3file)
    audioclip.close()
    videoclip.close()

def engine(link):
    l = link.split("\\")
    name = l[-1].split('.')[0]
    mp4tomp3(link, name + ".mp3")
    return str(name) + ".mp3"
