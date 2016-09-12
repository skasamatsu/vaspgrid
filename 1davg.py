import sys

file1 = open(raw_input("Input x-y data 1 "),"r")
file2 = open(raw_input("Input x-y data 2 "),"r")
fileout = open(raw_input("Output file name "), "w")

sys.stdout = fileout

dat1 = file1.readlines()
dat2 = file2.readlines()

for i in range(len(dat1)):
    dat1[i] = dat1[i].split()
    dat2[i] = dat2[i].split()
    for j in range(len(dat1[i])):
        dat1[i][j] = float(dat1[i][j])
        dat2[i][j] = float(dat2[i][j])
    print dat1[i][0], (dat1[i][1]+dat2[i][1])/2.0
