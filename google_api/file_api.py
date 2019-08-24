#!/usr/bin/env python3

from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaIoBaseDownload
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

class GdFile:
    def __init__(self, ):
        drive_service = None
        self.md5checksum = None

    def GetService(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build('drive', 'v3', credentials=creds)
        
        #file_name = 'TMS_FW_FreeRTOS.hex'
    
    def checkFileChange(self, old_check, service, file_Id):
        files = service.files()
        check = files.get(fileId=file_Id, fields="md5Checksum").execute()
        print(check, old_check)
        ch =  check['md5Checksum'] != old_check
        return check['md5Checksum'], ch
        
    def Download(self, service, file_name='TMS_FW_FreeRTOS.hex', downloaded_fw='FW.hex'):
        files = service.files().list().execute()['files']
        for f in files:
            if f['name'] == file_name:
                file_id = f['id']
                #fh = io.BytesIO()
                fh = io.FileIO(downloaded_fw, 'wb')
                request = service.files().get_media(fileId=file_id)
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))
                return file_id


if __name__ == "__main__":
    f = GdFile()
    service = f.GetService()
    while True:
        time.sleep(1)
        if f.md5checksum == None:
            file_id = f.Download(service)
            f.md5checksum = f.checkFileChange(f.md5checksum, service, file_id)[0]
        else:
            if f.checkFileChange(f.md5checksum, service, file_id)[1]:
                file_id = f.Download(service)
                f.md5checksum = f.checkFileChange(f.md5checksum, service, file_id)[0]
            else:
                print('NOP')

