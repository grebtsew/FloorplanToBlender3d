from api.api import Api

class Put(Api):

    def create_file(self):
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'PUT',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        print("\nform:", str(form))
        print("\nform['file'].filename:", form['file'].filename)
        filename = form['file'].filename
        data = form['file'].file.read()
        open("/tmp/%s" % filename, "wb").write(data)
        print('\ndata:', data)
        """

    def send(self, api_ref, data, *args):
        # id and hash correct exist?
        if((data['id'],data['hash'], False) in self.shared.all_ids ):
        
            # image format supported?
            
            # insert (data['id'],data['hash'], True)
            message = "File uploaded!"
        elif((data['id'],data['hash'], True) in self.shared.all_ids ):
            message = "File with same name already exist!"
        else:
            message = "Wrong ID or HASH!"
        return message

    def sendcreate(self, *args):
        """send image to server and start transform process"""
        return str(self.shared.images)
