'''
Application from a .kv
======================

The root application is created from the corresponding .kv. Check the test.kv
file to see what will be the root widget.
'''
import os.path
import kivy
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


url = 'https://8bd5758e5441f0f5646f867511295d20d4958a06.googledrive.com/host/0ByfS5eFr0zbkSS1Vd3Z1N3lZZ2M/test.db'

def get_local_file():
    save_dir = appVar.user_data_dir
    local_filename = url.split('/')[-1]
    local_file = os.path.join(save_dir, local_filename)
    return local_file

class WelcomeScreen(Screen):
    
    def got_db(self,req,results):
        self.manager.current = 'question'
    def got_redirect(self,req,result):
        print result
    def got_failure(self,req,failure):
        print failure
    def got_error(self,req,failure):
        print failure
    
    def download_db(self):
        req = UrlRequest(url,on_success=self.got_db, on_redirect=self.got_redirect, on_failure=self.got_failure, on_error=self.got_error,
                 file_path=get_local_file())

class QuestionScreen(Screen):
    question_widget = ObjectProperty()
    current_question_id = -1

    def get_next_question(self):
        rs = (None, None)
        conn = sqlite3.connect(get_local_file())
        try:
            c = conn.cursor()
            c.execute( 'SELECT question, id FROM questions where id > '+str(self.current_question_id)+' LIMIT 1')
            rs = c.fetchone()   
        except sqlite3.Error, e:
            print e
        finally:
            conn.close()
        
        data = None
        if rs:
            self.current_question_id = rs[1]
            data = {'question': rs[0], 'id': rs[1]}
        
        return data
    
    def display_question(self):
        random_question = self.get_next_question()
        if random_question:
            self.question_widget.text = r'"%s"%s-- %s' % \
                (random_question['question'], '\n' * 2, random_question['id'])
        else:
            self.manager.current = 'home'

class RootScreen(ScreenManager):
    pass

class TestApp(App):
   def build(self):
        return RootScreen()

if __name__ == '__main__':
    appVar = TestApp()
    TestApp().run()
