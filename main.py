import sys
import shutil
from urllib.parse import urlparse

import requests


def download_video(url, file_name):
    with requests.get(url=url, stream=True) as r:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        print('please give me reddit url')

    url = argv[1]
    meta_data_url = f'{url}.json'

    res = requests.get(url=meta_data_url)
    if res.status_code != 200:
        print('invalid url or service is down')    

    meta_data = res.json()
    main_data = meta_data[0]['data']['children'][0]['data']
    
    title = main_data['title']
    original_post = main_data['url_overridden_by_dest']
    thumbnail = main_data['thumbnail']
    crosspost_parent_list = main_data['crosspost_parent_list']
    secure_media = crosspost_parent_list[0]['secure_media']
    reddit_video = secure_media.get('reddit_video')
    sub_reddit = crosspost_parent_list[0]['subreddit_name_prefixed']
    if not reddit_video:
        print('has no video')
    
    is_gif = reddit_video['is_gif']
    video_url = reddit_video['fallback_url']
    
    u_parse = urlparse(original_post)
    post_id = u_parse.path[1:]
    audio_url = f'https://v.redd.it/{post_id}/DASH_audio.mp4'

    print({
        'id': post_id,
        'title': title,
        'sub_reddit': sub_reddit,
        'thumbnail': thumbnail,
        'is_gif': is_gif,
        'original_post': original_post,
        'video_url': video_url,
        'audio_url': audio_url,
    })
    download_video(video_url, 'video.mp4')
    download_video(audio_url, 'audio.mp4')
