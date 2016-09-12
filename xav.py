# Beware! Only tested for non-spin-polarized case

import re
import sys
import rlcompleter
import readline
#from numpy import *
from enterfi import enterfi
from outputfi import outputfi

gridfname = enterfi("Enter VASP field data (CHGCAR, LOCPOT, etc.)")
outfname = outputfi("Enter output file name ")
gridfi = open(gridfname,"r")

gridfi.readline() # Skip system name

# Read lattice scaling constant
li = gridfi.readline().split() 
scale = [0.0,0.0,0.0]
if len(li) == 1:
    li = float(li[0])
    for i in range(3):
        scale[i] = li
else:
    if len(li) == 3:
        for i in range(3):
            scale[i] = float(li[i])

# Read lattice vectors
latcons = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
for i in range(3):
    li = gridfi.readline().split()
    for j in range(3):
        latcons[i][j] = float(li[j])*scale[j]

print latcons

# Is this lattice orthorhombic in z direction?
assert latcons[0][2] <= 1.0e-8
assert latcons[1][2] <= 1.0e-8
assert latcons[2][0] <= 1.0e-8
assert latcons[2][1] <= 1.0e-8

# Read number of atoms
# Is this from vasp5 or vasp4? vasp5 has element names on the sixth line
# while vasp 4 does not.
li = gridfi.readline().split()
if re.match("[0-9]",li[0].strip()):
    # It's vasp4
    nspecs = len(li)
    natoms = 0
    for i in range(nspecs):
        li[i] = int(li[i])
        natoms = natoms + li[i]
else:
    # It's vasp5. Read one more line.
    li = gridfi.readline().split()
    nspecs = len(li)
    natoms = 0
    for i in range(nspecs):
        li[i] = int(li[i])
        natoms = natoms + li[i]

print natoms

gridfi.readline() # Skip one line. It probably says "Direct".
for i in range(natoms+1):
    gridfi.readline() # Skip the atom coordinates plus 1 blank line
# Read the grid dimensions
grid = gridfi.readline().split()
for i in range(len(grid)):
    grid[i]=int(grid[i])
ngrid = grid[0] * grid[1] * grid[2]
dz = latcons[2][2]/grid[2]
dx = latcons[0][0]/grid[0]

# Now read the rest of the file
data=gridfi.read().split()
for i in range(ngrid):
    data[i]=float(data[i])

xavg=[0.0]*grid[0]
print len(data)
print ngrid

for i in range(grid[1]*grid[2]):
    for j in range(grid[0]):
        xavg[j]+= data[i*grid[0]+j]
        #xavg[j]+=data[i*grid[1]*grid[2]+j]
        

for i in range(len(xavg)):
    xavg[i] = xavg[i]/grid[1]/grid[2]
        
outfi = open(outfname,"w")
for i in range(len(xavg)):
    outfi.write(str(dx*i) + "  " + str(xavg[i]) + "\n")
    
#print zavg
