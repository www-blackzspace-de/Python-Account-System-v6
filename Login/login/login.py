import json
import os
import sys 
import os.path
import logging

import mysql.connector
import hashlib
import time

from time import sleep
from cryptography.fernet import Fernet


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QMessageBox

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot




import ui
from ui import Ui_MainWindow








key_file = ".config/key.key"
input_file = ".config/encrypted"

with open(key_file, "rb") as k:
    key = k.read()
    
    
with open(input_file, "rb") as f:
    data = f.read()
    
fernet = Fernet(key)
decrypted = fernet.decrypt(data)
config = json.loads(decrypted)



ip = config['ip']
userx= config['user']
passwordx = config['password']
databasex = config['database']



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.window = None
        
        
        self.login_Button.clicked.connect(self.login)
        self.hyperlink_register.setOpenExternalLinks(True)
        
      
    
    

        
        
        
    def login(self):
        username = self.username_Input.text()
        password = self.password_Input.text()
        hashed = hashlib.sha256(password.encode()).hexdigest()
        os.chdir(".data/.r3m3mb3r")
        
        if self.checkBox_remember.isChecked():
            with open("remember.json", "w") as f:
                json.dump({"username": username, "password": hashed}, f)
                key = Fernet.generate_key()
                with open('key.key','wb') as file:
                    file.write(key)

                with open('key.key','rb') as file:
                    key = file.read()

                with open('remember.json','rb') as f:
                    data = f.read()

                fernet = Fernet(key)
                encrypted = fernet.encrypt(data)

                with open('encrypted','wb') as f:
                    f.write(encrypted)
                    
                os.remove("remember.json")
        

      
   
        
        
        if (username=="" or username=="UserID") or (password=="" or password=="Password"):
            self.consoleLog.append("Console >Error")
            
        else:
            try:
                mydb=mysql.connector.connect(host=ip, user=userx, password=passwordx, database=databasex)
                mycursor=mydb.cursor()
                self.consoleLog.append("Console > Connected to db!")
                self.progressBar.setValue(50)
                
                
               
        
            except:
                self.consoleLog.append("Console > Not connected to db!")
                self.progressBar.setValue(50)
                return
            
          

                
            command="use blackzspacededbx"
            mycursor.execute(command)
            
            command="select * from login_table where username=%s and password=%s"
            mycursor.execute(command, (username, hashed))
            
            
            result = mycursor.fetchone()
            
            
           
            if result==None:
               self.consoleLog.append("Console > Invalid userid or password")
               self.progressBar.setValue(100)
               self.progressBar.setValue(0)
               
            else:
                self.consoleLog.append("Console > Successfully loggedIn !")
                self.progressBar.setValue(100)
                
                


        
        
  


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()