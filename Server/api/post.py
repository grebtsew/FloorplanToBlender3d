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

    def transform(self, *args):
        """Transform Image to Object"""
        return str(self.shared.images)

