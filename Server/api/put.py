from api.api import Api

class Put(Api):
    # TODO: fix data variable format instead for indexing lists!

    def create_file(self, data, file):
        """Write incoming data to file"""
        file_path = self.shared.parentPath+"/"+self.shared.imagesPath + "/" + data['id'][0] + data['format'][0]
        open(file_path, "wb").write(file)

    def create(self, api_ref, data, file, *args):
        # id and hash correct exist?
        if((data['id'][0],data['hash'][0], False) in self.shared.all_ids ):

            # image format supported?
            if data['format'][0] in self.shared.supported_image_formats:
                
                self.create_file(data, file)

                # update saved file status
                index = self.shared.all_ids.index((data['id'][0],data['hash'][0], False))
                self.shared.all_ids[index] = (data['id'][0],data['hash'][0], True)
                message = "File uploaded!"
                
                # trigger index update for gui!
                self.shared.reindex_files()
            else:
                message = "Image format not supported!"
            
        elif((data['id'][0],data['hash'][0], True) in self.shared.all_ids ):
            message = "File with same name already exist!"
        else:
            message = "Wrong ID or HASH!"
        return message

    def createandtransform(self,api_ref, data,file,  *args):
        """send image to server and start transform process"""
        message = self.create(data,file)

        _id = self.shared.get_id(data['id'])
        if _id is not None and _id[2]:
            if(data['format'] in self.shared.supported_blender_formats):
                Create(data=data, shared_variables = self.shared).start()
                message += "TransformProcess started! Query Process Status for more Information."
            else:
                message += "Output Format not supported!"
        else:
            message += "File doesn't exist!"
            self.shared.bad_client_event(self.client)
        return message
