from api.api import Api
import json
import shutil
import os

def sendFileHeaders(_api_ref, file):
    _api_ref.send_response(200)
    _api_ref.send_header("Content-type", 'multipart/form-_data')
    fs = os.fstat(file.fileno())
    _api_ref.send_header("Content-Length", str(fs[6]))
    _api_ref.send_header("Last-Modified", _api_ref.date_time_string(fs.st_mtime))
    _api_ref.end_headers()

def returnFile( path, _api_ref):
    with open(path, "rb") as file:
        sendFileHeaders(_api_ref, file)
        shutil.copyfileobj(file, _api_ref.wfile)
    return "File sent!"

class Get(Api):

    def __init__(self,  client ,  shared_variables ) :
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

    def info(self, _api_ref, _data,*args, **kwargs) -> str:
        return '\n'.join([
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (_api_ref.client_address,
                _api_ref.address_string()),
            'command=%s' % _api_ref.command,
            'path=%s' % _api_ref.path,
            '_data=%s' % _data,
            'request_version=%s' % _api_ref.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % _api_ref.server_version,
            'sys_version=%s' % _api_ref.sys_version,
            'protocol_version=%s' % _api_ref.protocol_version,
            '',
            'supported_image_formats=%s' % str(self.shared.supported_image_formats),
            'supported_blender_formats=%s' % str(self.shared.supported_blender_formats)
            ])

    def process(self, pid:str, *args, **kwargs) -> str:
        """Get a specific process"""
        p = self.shared.get_process(pid)
        if p is None:
            return "Process does not exist!"
        else:
            return json.dumps(p)

    def all(self, *args, **kwargs) -> str:
        """Return all files currently managed by server"""
        return json.dumps(self.shared.all_files)

    def images(self, *args, **kwargs) -> str:
        """Get all images on server"""
        return json.dumps(self.shared.images)

    def objects(self, *args, **kwargs) -> str:
        """Get all objects on server"""
        return json.dumps(self.shared.objects)

    def processes(self, *args, **kwargs) -> str:
        """Get all processes"""
        return json.dumps(self.shared.all_processes)
    
    def image(self, _api_ref, id:str, *args, **kwargs) -> str:
        """Return imagefile of id specified in _data"""
        # check that file exist
        return returnFile(self.shared.get_image_path(id), _api_ref)
        
    def object(self, _api_ref, id:str, oformat:str, *args, **kwargs) -> str:
        """Return objectfile of id specified in _data"""
        # check if file exist
        obj = self.shared.get_object_path(id, oformat)
        if obj is None:
            return "No such object exists!"
        else:
            return returnFile(obj, _api_ref)