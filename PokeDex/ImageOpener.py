import subprocess
import os
import sys

def ImageOpener(ImageName):
    #print('ImageName:'+ImageName)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    PythonExe=os.path.join(BASE_DIR,'PokeDex','PokeDexVenv','Scripts','python.exe')
    OpenImageScript=os.path.join(BASE_DIR,'PokeDex','OpenImageInternal.py')
    ImagePath=os.path.join(BASE_DIR,'PokeDex','Images',ImageName)

    FullArg=PythonExe+' '+OpenImageScript+' '+ImagePath

    #print(FullArg)
    subprocess.run(FullArg)

if __name__ == "__ImageOpener__":
    ImageOpener(sys.argv[1])