from shared_variables import shared_variables
from api.api import Api
from process.create import Create
from config.file_handler import FileHandler

class Post(Api):

    def __init__(self, client ,  shared_variables ):
        super().__init__(client, shared_variables)
        # All all viable functions here!
        self.dispatched_calls["create"] = self.create
        self.dispatched_calls["remove"] = self.remove
        self.dispatched_calls["transform"] = self.transform
        

    def create(self, *args):
        """Create new specific file name/id and hash"""
        tmp_id = None

        while self.shared.id_exist(tmp_id) or tmp_id is None: 
            tmp_id = self.shared.id_generator()
        
        pair = (tmp_id,self.shared.hash_generator(tmp_id), False)
        self.shared.all_ids.append(pair)

        return str(pair)

    def remove(self, api_ref, data, *args):
        """Remove existing file id"""
        fs = FileHandler()
        # This will remove all files related to id
        for file in self.shared.all_files:
            if data["id"] in file:
                for f in self.shared.get_id_files(data["id"]):    
                    fs.remove(f)

        self.shared.reindex_files()
        return "Removed id!"

    def transform(self, api_ref, data, *args):
        """Transform Image to Object"""
        _id = self.shared.get_id(data['id'])
        if _id is not None and _id[2]:
            if(data['oformat'] in self.shared.supported_blender_formats):
                Create(data=data, shared_variables = self.shared).start()
                message = "TransformProcess started! Query Process Status for more Information."
            else:
                message = "Format not supported!"
        else:
            message = "File doesn't exist!"
            self.shared.bad_client_event(self.client)
        return message

