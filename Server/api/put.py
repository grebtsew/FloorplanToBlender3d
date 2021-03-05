from api.api import Api
from api.post import Post # needed to call transform function

def create_file(ref, data, file):
        """Write incoming data to file"""
        file_path = ref.shared.parentPath+"/"+ref.shared.imagesPath + "/" + data['id'] + data['iformat']
        open(file_path, "wb").write(file)

class Put(Api):
    
    def __init__(self,  client,  shared_variables) :
        super().__init__(client, shared_variables)
        # All all viable functions here!
        self.dispatched_calls["create"] = self.create
        self.dispatched_calls["createandtransform"] = self.createandtransform
    
    def create(self, api_ref, data, file, *args):
        # id and hash correct exist?
        status = True
        if((data['id'],data['hash'], False) in self.shared.all_ids ):

            # image format supported?
            if data['iformat'] in self.shared.supported_image_formats:
                
                create_file(self, data, file)

                # update saved file status
                index = self.shared.all_ids.index((data['id'],data['hash'], False))
                self.shared.all_ids[index] = (data['id'],data['hash'], True)
                message = "File uploaded!"
                
                # trigger index update for gui!
                self.shared.reindex_files()
            else:
                message = "Image format not supported!"
                status = False
        elif((data['id'],data['hash'], True) in self.shared.all_ids ):
            message = "File with same name already exist!"
            status = False
        else:
            message = "Wrong ID or HASH!" 
            status = False
        return message, status

    def createandtransform(self,api_ref, data,file,  *args):
        """send image to server and start transform process"""
        message, status = self.create(api_ref, data,file)
        message += " "
        if status:
            message += Post(self.client, self.shared).transform(api_ref, data,file)
        return message, status
