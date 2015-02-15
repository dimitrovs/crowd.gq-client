'''
Application from a .kv
======================

The root application is created from the corresponding .kv. Check the test.kv
file to see what will be the root widget.
'''
import os.path
import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.app import App

class WelcomeScreen(BoxLayout):
    def got_db(self,req,results):
        print results
    def got_redirect(self,req,result):
        print result
    def got_failure(self,req,failure):
        print failure
    def got_error(self,req,failure):
        print failure
    
    def download_db(self):
        url = 'https://8bd5758e5441f0f5646f867511295d20d4958a06.googledrive.com/host/0ByfS5eFr0zbkSS1Vd3Z1N3lZZ2M/nwind28.db'
        save_dir = appVar.user_data_dir
        print appVar.user_data_dir
        local_filename = url.split('/')[-1]
        local_file = os.path.join(save_dir, local_filename)
        req = UrlRequest(url,on_success=self.got_db, on_redirect=self.got_redirect, on_failure=self.got_failure, on_error=self.got_error,
                 file_path=local_file)
    
class TestApp(App):
    pass

if __name__ == '__main__':
    appVar = TestApp()
    TestApp().run()
