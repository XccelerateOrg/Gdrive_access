import psycopg2
import os
from dotenv import load_dotenv
from gdrive_app.file_migrate import move_file_to_folder, get_id, get_videos
from gdrive_app.utilities.authenticate import authenticate


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

    print("Total video paths are:  ", len(videos))

    for video in videos:
        origin = get_id(video[2])
        destin = get_id(video[4])
        videoName = video[3]
        tag = video[1]

        vid_lst = get_videos(authenticate(), origin, videoName)

        print('*' * 15)
        print("Transferring Pathname: " + videoName)
        print("Origin Folder ID: " + origin)
        print("Destination Folder ID: " + destin)
        print("Tag: " + tag)
        print("Transferred Videos: ")

        for items in vid_lst:
            print("Video: " + items["name"])
            move_file_to_folder(service=authenticate(),
                                file_id=items['id'],
                                folder_id=destin)
    cursor.close()
    conn.close()
