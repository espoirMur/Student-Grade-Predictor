import sys
import os
cwd = os.getcwd()
sys.path.insert(0,cwd+"/codes/")
reload(sys)
sys.setdefaultencoding('utf8') #for ascii decoder in notes
print sys.path
