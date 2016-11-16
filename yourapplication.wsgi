# make sure our folder is in the path
import sys
sys.path.insert(0, '/www/python.karldenby.com/python')
sys.path.insert(1, '/www/python.karldenby.com/python/bootstrap')

# import our program
from myapp import app as application
