from re import L
from minio import Minio
import config_with_yaml as config
import os

class RepoManager:

    def displayConfig(self):
        print("  " + str(self.cfg.getProperty(f"{self.config_name}.Server.ip")))
        print("  " + str(self.cfg.getProperty(f"{self.config_name}.Server.access_key")))
        print("  " + str(self.cfg.getProperty(f"{self.config_name}.Server.secret_key")))
        print("  " + str(self.cfg.getProperty(f"{self.config_name}.Server.region")))
        print("  " + str(self.cfg.getProperty(f"{self.config_name}.Server.secure")))


    def getClient(self, cfg):
        client = Minio(
            cfg.getProperty(f"{self.config_name}.Server.ip"),
            access_key=cfg.getProperty(f"{self.config_name}.Server.access_key"),
            secret_key=cfg.getProperty(f"{self.config_name}.Server.secret_key"),
            region=cfg.getProperty(f"{self.config_name}.Server.region"),
            secure=cfg.getProperty(f"{self.config_name}.Server.secure")
        )

        return client


    def createBucket(self, userId):
        if not self.client.bucket_exists(userId):
            self.client.make_bucket(userId)
        else:
            pass

    def removeBucket(self, userId):
        self.client.remove_bucket(userId)

    def getUsersMedia(self, userId):
        objects = self.client.list_objects(userId, recursive=True)
        return objects

    def listUsersMedia(self, userId):
        results = []
        objects = self.client.list_objects(userId, recursive=True)
        for obj in objects:
            results.append(obj.object_name)
        return results

    def downloadMedia(self, userId, objectFullPath, localFileName):
        self.client.fget_object(userId, objectFullPath, localFileName)

    def uploadMedia(self, userId, remoteObjectFullPath, localFilename):
        self.client.fput_object(userId, remoteObjectFullPath, localFilename)

    def removeMedia(self, userId, remoteObjectFullPath):
        # Remove object.
        self.client.remove_object(userId, remoteObjectFullPath)

    def __init__(self, cfg, config_name):
        self.cfg = cfg
        self.config_name = config_name
        self.client = self.getClient(cfg)
        self.displayConfig()
        # self.displayConfig()


cfg = config.load("../minio_config.yml")

MINIO_CONFIG_NAME = os.environ.get('CONTENT_MANAGER_CONFIG','')
MINIO_BUCKET_NAME = os.environ.get('CONTENT_MANAGER_BUCKET','')

if MINIO_CONFIG_NAME != '' and MINIO_BUCKET_NAME != '' and MINIO_CONFIG_NAME in cfg:
    rm = RepoManager(cfg, MINIO_CONFIG_NAME) # 'frontend_local_view'
else:
    print('######## WARNING: MINIO SETUP NOT IN USE ########')
    print('')
    print(f'Check parameters: {MINIO_BUCKET_NAME} and {MINIO_CONFIG_NAME}')
    print('')
    print('######## WARNING: MINIO SETUP NOT IN USE ########')
    rm = None

def upload_to_minio(ls_files, path):
    if rm:
        try:
            rm.createBucket(MINIO_BUCKET_NAME)
            for file in ls_files:
                file = os.path.join(path,file)
                upload_path = file.split('../')[-1]
                rm.uploadMedia(MINIO_BUCKET_NAME, upload_path, file)
        except Exception as exception: 
            print(exception)

def download_from_minio(ls_files, path):
    if rm:
        rm.createBucket(MINIO_BUCKET_NAME)
        for file in ls_files:
            file = os.path.join(path,file)
            upload_path = file.split('../')[-1]
            rm.downloadMedia(MINIO_BUCKET_NAME, upload_path, file)

def remove_from_minio(ls_files, path):
    if rm:
        rm.createBucket(MINIO_BUCKET_NAME)
        for file in ls_files:
            file = os.path.join(path,file)
            upload_path = file.split('../')[-1]
            rm.removeMedia(MINIO_BUCKET_NAME, upload_path)

def remove_folder_from_minio(path):
    if rm:
        delete_object_list = rm.client.list_objects(MINIO_BUCKET_NAME, path, recursive=True)
        errors = rm.client.remove_objects(MINIO_BUCKET_NAME, delete_object_list)
        for error in errors:
            print("error occured when deleting object", error)