import sys, os
def outputfi(prompt=""):
    while True:
        filename = raw_input(prompt+"\t").strip()
        if os.path.exists(filename):
            yesno = raw_input("File already exists. Overwrite (y/n)?\t").strip().lower()
            while True:
                if yesno == "y":
                    break
                elif yesno == "n":
                    break
                else:
                    yesno = raw_input("Please enter y or n\t").strip().lower() 
                    continue
            if yesno == "y":
                break
            elif yesno == "n":
                continue
            else:
                print "Error. This shouldn't happen."
                raise IOError
        else:
            break
    return filename
