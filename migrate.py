import os
from pprint import pprint
import time

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name[-3:] == ".py":
            with open(os.path.join(root, name), 'r') as f:
#                print "file: " + os.path.join(root, name)
                lines = f.readlines()
                f.close()
#                print lines
                for lineNum in xrange(len(lines)):
                    lines[lineNum] = lines[lineNum].replace("from app", "from stuybulletin")
                    lines[lineNum] = lines[lineNum].replace("import app", "import stuybulletin")
                    if name not in ["application.py", "__init__.py"]:
                        lines[lineNum] = lines[lineNum].replace("app.", "stuybulletin.")

#                print lines
                with open(os.path.join(root, name), 'w') as g:
                    g.write(''.join(lines))
                    g.close()
