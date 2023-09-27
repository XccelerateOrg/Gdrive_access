from googleapiclient.errors import HttpError


def get_folder_id(service, folder_name):
    folder = (service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and fullText contains '{folder_name}'",
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
        service = service
        print("Moving " + file_id + " to " + folder_id)
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = service.files().update(fileId=file_id, addParents=folder_id,
                                      removeParents=previous_parents,
                                      fields='id, parents').execute()
        return file.get('parents')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None

    '''if request.method == 'POST':
    origin = get_id(request.form["folder"])
    video = request.form["video"]
    destin = get_id(request.form["designate"])
    vid_lst = get_videos(authenticate(), origin, video)
    print(origin+video+destin+vid_lst)

    for items in vid_lst:
        move_file_to_folder(service=authenticate(),
                            file_id=items['id'],
                            folder_id=destin)'''