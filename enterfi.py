import sys, os
def enterfi(prompt=""):
    while True:
        filename = raw_input(prompt+"\t").strip()
        if os.path.exists(filename):
            break
        else:
            print "File does not exist. Try again:"
    return filename
