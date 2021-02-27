from shared_variables import shared_variables
from api.api import Api


class Post(Api):
    
    def create(self, *args):
        """Create new specific file name/id and hash"""
        tmp_id = None

        while self.shared.id_exist(tmp_id) or tmp_id is None: 
            tmp_id = self.shared.id_generator()
        
        pair = (tmp_id,self.shared.hash_generator(tmp_id), False)
        self.shared.all_ids.append(pair)

        return str(pair)

    def remove(self, *args):
        """Remove existing file id"""
        return str(self.shared.images)

    def transform(self, api_ref, data, *args):
        """Transform Image to Object"""

        _id = self.shared.get_id(data['id'])
        if _id is not None and _id[2]:
            if(data['format'] in self.shared.supported_blender_formats):
                Create(data=data, shared_variables = self.shared).start()
                message = "TransformProcess started! Query Process Status for more Information."
            else:
                message = "Format not supported!"
        else:
            message = "File doesn't exist!"
            self.shared.bad_client_event(self.client)
        return message

