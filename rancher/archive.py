import os

from data_storage.azure_blob import AzureBlobResource
from data_storage.exceptions import ResourceAlreadyExist

from . import settings
import files

_blob_resource = None
def get_blob_resource():
    """
    Return the blob resource client
    """
    global _blob_resource
    if _blob_resource is None:
        _blob_resource = AzureBlobResource(
            settings.RESOURCE_NAME,
            settings.AZURE_CONNECTION_STRING,
            settings.AZURE_CONTAINER,
            archive=False,
            resource_base_path="{}/{}".format(settings.RESOURCE_NAME,settings.RANCHER_CLUSTER),
            logical_delete=True
        )
    return _blob_resource

def need_archive(path):
    file_folder,file_name = os.path.split(path)
    if file_name[0] == ".":
        return False
    else:
        return settings.FILE_RE.search(file_name)

def archive():
    files.archive(get_blob_resource(),folder=settings.ARCHIVE_FOLDER,recursive=True,reserve_folder=settings.RESERVE_FOLDER,archive=False,file_filter=need_archive)