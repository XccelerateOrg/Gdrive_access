import io
import concurrent
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from googleapiclient.http import MediaIoBaseDownload
from tabulate import tabulate


def get_files(service, name=None):
    files_list = []
    next_page_token = None
    if not name:
        while True:
            results = service.files().list(spaces='drive',
                                           supportsAllDrives=True,
                                           fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)",
                                           includeItemsFromAllDrives=True,
                                           pageToken=next_page_token).execute()
            files_list.extend(results.get('files', []))
            next_page_token = results.get('nextPageToken', None)
            if next_page_token is None:
                break
    else:
        while True:
            results = service.files().list(
                q=f"name contains '{name}'",
                spaces='drive',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)",
                pageToken=next_page_token
            ).execute()
            files_list.extend(results.get('files', []))
            next_page_token = results.get('nextPageToken', None)
            if next_page_token is None:
                break
    return files_list


def get_all_files(service):
    all_files = get_files(service=service)
    list_files(all_files)
    return all_files


def get_file_by_name(service, name="", verbose=False):
    all_files = get_files(service=service, name=name)
    if verbose:
        list_files(all_files)
    return all_files


def list_files(items=None):
    if not items:
        print('No files.')
    else:
        rows = []
        for item in items:
            idx = item["id"]
            name = item["name"]
            try:
                parents = item["parents"]
            except:
                parents = ""
            mime_type = item["mimeType"]
            modified_time = item["modifiedTime"]
            rows.append((idx, name, parents, mime_type, modified_time))
            table = tabulate(rows, headers=["ID", "Name", "Parent", "Type", "Modified Time"])
            print(table)


def download_bytesio(service, file_obj, destination=None):
    # print(f"Downloading {file_obj['name']}")
    request = service.files().export_media(fileId=file_obj['id'],
                                           mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request, chunksize=2048 * 2048)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    if destination:
        with open(destination, "wb") as f:
            f.write(file.getvalue())
    # print(f"Download finished {file_obj['name']}!")
    return file

