from api.api import Api
import json
import shutil
import os

def sendFileHeaders(api_ref, file):
    api_ref.send_response(200)
    api_ref.send_header("Content-type", 'multipart/form-data')
    fs = os.fstat(file.fileno())
    api_ref.send_header("Content-Length", str(fs[6]))
    api_ref.send_header("Last-Modified", api_ref.date_time_string(fs.st_mtime))
    api_ref.end_headers()

def returnFile( path, api_ref):
    with open(path, "rb") as file:
        sendFileHeaders(api_ref, file)
        shutil.copyfileobj(file, api_ref.wfile)
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

    def info(self, api_ref, parsed_data, parsed_path,*args):
        return '\n'.join([
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (api_ref.client_address,
                api_ref.address_string()),
            'command=%s' % api_ref.command,
            'path=%s' % api_ref.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % api_ref.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % api_ref.server_version,
            'sys_version=%s' % api_ref.sys_version,
            'protocol_version=%s' % api_ref.protocol_version,
            '',
            'supported_image_formats=%s' % str(self.shared.supported_image_formats),
            'supported_blender_formats=%s' % str(self.shared.supported_blender_formats)
            ])

    def process(self, api_ref, data, *args):
        p = self.shared.get_process(data['pid'])
        if p is None:
            return "Process does not exist!"
        else:
            return json.dumps(p)

    def all(self, *args):
        """Return all files currently managed by server"""
        return json.dumps(self.shared.all_files)

    def images(self, *args):
        return json.dumps(self.shared.images)

    def objects(self, *args):
        return json.dumps(self.shared.objects)

    def processes(self, *args):
        return json.dumps(self.shared.all_processes)
    
    def image(self, api_ref, data, *args):
        """Return imagefile of id specified in data"""
        # check that file exist
        return returnFile(self.shared.get_image_path(data["id"]), api_ref)
        
    def object(self, api_ref, data, *args):
        """Return objectfile of id specified in data"""
        # check if file exist
        obj = self.shared.get_object_path(data["id"], data["oformat"])
        if obj is None:
            return "No such object exists!"
        else:
            return returnFile(obj, api_ref)

