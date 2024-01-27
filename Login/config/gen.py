import os
import sys 
import cryptography 
import logging
import cmd
from cryptography.fernet import Fernet
from cmd import Cmd


from os.path import *

logging.basicConfig(filemode="w", filename="config-gen.logs", level="DEBUG")
print("Console > ConfigGen started...")


class ConfigGenerator(cmd.Cmd):
    """ MAIN CLASS"""
    
    prompt = "ConfigGen > "
    
    doc_header = ""
    undoc_header = ""
    
    
    
    def do_run(self, line):
        print("Generating config...")
        key = Fernet.generate_key()
        with open('key.key','wb') as file:
            file.write(key)

#this just opens your 'key.key' and assings the key stored there as 'key'
        with open('key.key','rb') as file:
            key = file.read()

#this opens your json and reads its data into a new variable called 'data'
        with open('config.json','rb') as f:
            data = f.read()

#this encrypts the data read from your json and stores it in 'encrypted'
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

#this writes your new, encrypted data into a new JSON file
        with open('encrypted','wb') as f:
            f.write(encrypted)
        
        

def loop():
    try:
        ConfigGenerator().cmdloop()
        
    except KeyboardInterrupt:
        sys.exit()
        
        
if __name__ == '__main__':
    loop()