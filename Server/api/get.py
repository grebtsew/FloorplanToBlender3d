from api.api import Api
import json
import shutil
import os

"""
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""


def sendFileHeaders(_api_ref, file):
    _api_ref.send_response(200)
    _api_ref.send_header("Content-type", "multipart/form-_data")
    fs = os.fstat(file.fileno())
    _api_ref.send_header("Content-Length", str(fs[6]))
    _api_ref.send_header("Last-Modified", _api_ref.date_time_string(fs.st_mtime))
    _api_ref.end_headers()


def returnFile(path, _api_ref):
    with open(path, "rb") as file:
        sendFileHeaders(_api_ref, file)
        shutil.copyfileobj(file, _api_ref.wfile)
    return "File sent!"


class Get(Api):
    def __init__(self, client, shared_variables):
        super().__init__(client, shared_variables)
        # All all viable functions here!
        self.dispatched_calls["info"] = self.info
        self.dispatched_calls["all"] = self.all
        self.dispatched_calls["image"] = self.image
        self.dispatched_calls["object"] = self.object
        self.dispatched_calls["images"] = self.images
        self.dispatched_calls["objects"] = self.objects
        self.dispatched_calls["process"] = self.process
        self.dispatched_calls["processes"] = self.processes
        self.dispatched_calls["configfiles"] = self.configfiles
        self.dispatched_calls["stackingfiles"] = self.stackingfiles
        self.dispatched_calls["configfile"] = self.configfile
        self.dispatched_calls["stackingfile"] = self.stackingfile

    def info(self, _api_ref, _data, *args, **kwargs) -> str:
        """Returns information about server implementation as JSON."""
        res = dict()
        res["client_address"] = _api_ref.client_address
        res["command"] = _api_ref.command
        res["path"] = _api_ref.path
        res["_data"] = _data
        res["request_version"] = _api_ref.request_version
        res["server_version"] = _api_ref.server_version
        res["sys_version"] = _api_ref.sys_version
        res["protocol_version"] = _api_ref.protocol_version
        res["supported_image_formats"] = self.shared.supported_image_formats
        res["supported_blender_formats"] = self.shared.supported_blender_formats
        return json.dumps(res)

    def process(self, pid: str, *args, **kwargs) -> str:
        """Get a specific process as JSON."""
        p = self.shared.get_process(pid)
        if p is None:
            return "Process does not exist!"
        else:
            return json.dumps(p)

    def all(self, *args, **kwargs) -> str:
        """Return all files currently managed by server as JSON."""
        return json.dumps(self.shared.all_files)

    def images(self, *args, **kwargs) -> str:
        """Get all images on server as JSON."""
        return json.dumps(self.shared.images)

    def stackingfiles(self, *args, **kwargs) -> str:
        """Get all stackingfiles on server as JSON"""
        return json.dumps(self.shared.stackingfiles)

    def configfiles(self, *args, **kwargs) -> str:
        """Get all configfiles on server as JSON"""
        return json.dumps(self.shared.configfiles)

    def objects(self, *args, **kwargs) -> str:
        """Get all objects on server as JSON."""
        return json.dumps(self.shared.objects)

    def processes(self, *args, **kwargs) -> str:
        """Get all processes as JSON."""
        return json.dumps(self.shared.all_processes)

    def image(self, _api_ref, id: str, *args, **kwargs) -> str:
        """Return imagefile of id specified in JSON."""
        # check that file exist
        return returnFile(
            self.shared.get_file_path(id, self.shared.imagesPath, self.shared.images),
            _api_ref,
        )

    def stackingfile(self, _api_ref, id: str, *args, **kwargs) -> str:
        """Get a stackingfile on server as JSON"""
        return returnFile(
            self.shared.get_file_path(
                id, self.shared.stackingPath, self.shared.stackingfiles
            ),
            _api_ref,
        )

    def configfiles(self, _api_ref, id: str, *args, **kwargs) -> str:
        """Get a configfile on server as JSON"""
        return returnFile(
            self.shared.get_file_path(
                id, self.shared.configPath, self.shared.configfiles
            ),
            _api_ref,
        )

    def object(self, _api_ref, id: str, oformat: str, *args, **kwargs) -> str:
        """Return objectfile of id specified in JSON."""
        # check if file exist
        obj = self.shared.get_object_path(id, oformat)
        if obj is None:
            return "No such object exists!"
        else:
            return returnFile(obj, _api_ref)
