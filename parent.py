import subprocess

def onestart():
    listen = subprocess.Popen("python wakeword.py resources/natmodel.umdl", shell=True)
    listen.wait()

onestart()
