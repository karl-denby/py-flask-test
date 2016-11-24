# make sure our folder is in the path
import sys

# Customize this
my_app_folder = '/var/www/mywebsite/python'

# Import our program
sys.path.insert(0, my_app_folder)
from myapp import app as application
