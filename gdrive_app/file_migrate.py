from googleapiclient.errors import HttpError
from datetime import datetime
import pytz


def get_folder_id(service, folder_name):
    folder = (
        service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and fullText contains '{folder_name}'",
                             spaces='drive',
                             supportsAllDrives=True,
                             includeItemsFromAllDrives=True,
                             fields="nextPageToken, files(id, name, parents)")
        .execute())
    folder_id = folder.get('files', [])
    if len(folder_id) == 0:
        return None
    elif len(folder_id) == 1:
        return folder_id[0]['id']
    else:
        return folder_id


def get_videos(service, folder_id, video):
    if folder_id:
        video = (service.files().list(
            q=f"mimeType='video/mp4' and '{folder_id}' in parents and fullText contains '{video}'",
            spaces='drive',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            fields="nextPageToken, files(id, name, parents, modifiedTime)")
                 .execute())
        items = video.get('files', [])
        return items
    else:
        return None


def get_id(url):
    url = url.split("folders/", 1)[1]
    return url


def move_file_to_folder(service, file_id, folder_id):
    try:
        # service = service
        print(f"\t[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}] Moving " + file_id + " to " + folder_id)
        file = service.files().get(fileId=file_id, fields='parents', supportsAllDrives=True).execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = service.files().update(fileId=file_id, addParents=folder_id,
                                      removeParents=previous_parents,
                                      fields='id, parents', supportsAllDrives=True).execute()
        return file.get('parents')

    except HttpError as error:
        print(f"[{datetime.now(pytz.utc).strftime('[%Y-%m-%d %H:%M:%S %z]')}] An error occurred: {error}")
        return None
