import py_cui
from VideoLauncher import VideoLauncher
from dotenv import load_dotenv

# load .env file
load_dotenv()

# Create the CUI with 7 rows 6 columns, pass it to the wrapper object, and start it
root = py_cui.PyCUI(7, 6)
root.set_title('ZVL')
s = VideoLauncher(root)
root.start()
