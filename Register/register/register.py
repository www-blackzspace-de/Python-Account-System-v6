import json
import os
import sys 
import os.path
import logging
import mysql.connector


import time

import hashlib
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




logging.basicConfig(filemode="w", filename="log.log", level="DEBUG")


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
        
                
        self.register_Button.clicked.connect(self.register)
    
    
    

        
        
    def register(self):
        
        username = self.username_Input_Registration.text()
        password = self.password_Input_Registration.text()
        email = self.email_Input_Registration.text()
        
        hashed = hashlib.sha256(password.encode()).hexdigest()
    
    
        
        if (username=="" or username=="UserID") or (password=="" or password=="Password"):
            self.consoleLog.append("Console >Error")
            
        else:
            try:
                mydb = mysql.connector.connect(host=ip, user=userx, password=passwordx)
                mycursor = mydb.cursor()
                self.consoleLog.append("Console > Connected to LoginServer!")
                self.progressBar.setValue(50)
                
                
            except:
                self.consoleLog.append("Console > Not connected to LoginServer!")
                self.progressBar.setValue(50)
        
        
        try:
            command="create database blackzspacededbx"
            mycursor.execute(command)
            
            command="use blackzspacededbx"
            mycursor.execute(command)
            
            command="CREATE TABLE IF NOT EXISTS `login_table` (`id` int(11) NOT NULL AUTO_INCREMENT,`username` varchar(50) NOT NULL,`password` varchar(255),`email` varchar(100) NOT NULL, NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;"
            mycursor.execute(command)
            
        except:
            mycursor.execute("use blackzspacededbx")
            mydb = mysql.connector.connect(host=ip, user=userx, password=passwordx, database=databasex)
            mycursor = mydb.cursor()
            
            command = "insert into login_table(username,password, email) values(%s,%s, %s)"
            mycursor.execute(command, (username, hashed, email))
            mydb.commit()
            mydb.close()
            self.consoleLog.append("Console > Registration succesfully!")
            self.progressBar.setValue(100)
        




if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()