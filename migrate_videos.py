import psycopg2
import os
from dotenv import load_dotenv
from gdrive_app.file_migrate import move_file_to_folder, get_id, get_videos
from gdrive_app.utilities.authenticate import authenticate
from datetime import datetime
import pytz


if __name__ == '__main__':
    _ = load_dotenv()
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_DATABASE"],
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"])

    cursor = conn.cursor()
    cursor.execute("""
                    SELECT id, tag, origin, video, destin, user 
                    FROM video_path
                    """)
    videos = cursor.fetchall()

    print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}]Total video paths are:  ", len(videos))

    for video in videos:
        print("==" * 50)
        print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}] Processing: {video[1]} ...")

        try:
            origin = get_id(video[2])
            destin = get_id(video[4])
            videoName = video[3]
            tag = video[1]
        except Exception as e:
            print(f"Wrong format entered! {e}. Skipping")
            continue

        try:
            vid_lst = get_videos(authenticate(), origin, videoName)

            print('*' * 50)
            print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}]Transferring Pathname: " + videoName)
            print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}]Origin Folder ID: " + origin)
            print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}]Destination Folder ID: " + destin)
            print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}]Tag: " + tag)
            print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}]Transferred Videos: ")

            for items in vid_lst:
                print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}]Video: " + items["name"])
                move_file_to_folder(service=authenticate(),
                                    file_id=items['id'],
                                    folder_id=destin)
        except Exception as e:
            print(f"Encountered exception {e}, Skipping")
    cursor.close()
    conn.close()
