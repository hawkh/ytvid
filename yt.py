import os
try:
    from pytube import YouTube
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
except:
    os.system("pip install pytube")
    os.system("pip install moviepy")
finally:
    from pytube import YouTube
    from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

path = 'C:/'
url = 'https://youtu.be/WjAPDofGg28'
streamsData = []
streamDataFormatted = []


def on_progress(stream, chunk, bytes_remaining):
    print("Downloaded", stream.filesize - bytes_remaining, "of", stream.filesize,
          round((stream.filesize - bytes_remaining) / stream.filesize * 100, 2), "%")


def on_complete(stream, file_path):
    print("Downloaded", stream.filesize, "bytes to", file_path)
    print("100.0 %")


def download(url):
    yt = YouTube(url, on_progress_callback=on_progress,
                 on_complete_callback=on_complete)
    streamsData = [x for x in yt.streams]
    audioStreams = [x for x in streamsData if x.type == 'audio'][-1]
    audioStreams.download(path, 'audio.mp3')
    for x in yt.streams:
        streamDataFormatted.append({
            'type': x.mime_type if x.mime_type else 'unknown',
            'res': x.resolution if x.resolution else 'unknown',
            'abr': x.abr if x.abr else 'unknown',
            'acodec': x.audio_codec if x.audio_codec else 'unknown',
            'vcodec': x.video_codec if x.video_codec else 'unknown',
            'filesize': str(int(x.filesize)//1024000)+'MB' if x.filesize else 'unknown',
            'progressive': x.is_progressive if x.is_progressive else 'unknown',
            # 'url': x.url if x.url else 'unknown'
        })
    index = 0
    for strm in streamDataFormatted:
        print(index, strm)
        index += 1
    while(1):
        x = input("Enter the index of the stream you want to download: ")
        try:
            x = int(x)
            if x < len(streamsData):
                break
            else:
                print("Invalid index")
        except:
            print("Invalid index")
    streamsData[x].download(path, 'video.mp4')
    # merge audio and video
    video = VideoFileClip(path + 'video.mp4')
    audio = AudioFileClip(path + 'audio.mp3')
    final_audio = CompositeAudioClip([audio])
    video.audio = final_audio
    video.write_videofile(path + 'final.mp4')
    print("Downloaded")

    # if type == 'audio':
    #     yt.streams.filter(only_audio=True).first().download(path)
    # elif type == 'video':
    #     yt.streams.filter(res=res).first().download(path)


if name == "main":
    download(url)