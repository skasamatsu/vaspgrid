# Beware! Only tested for non-spin-polarized case

import re
import sys
import rlcompleter
import readline
from numpy import *
from enterfi import enterfi
from outputfi import outputfi

gridfname = enterfi("Enter VASP field data (CHGCAR, LOCPOT, etc.)")
outfname = outputfi("Enter output file name ")
gridfi = open(gridfname,"r")
outfi_chg = open(outfname+"_tot",'w')
outfi_mag = open(outfname+"_mag",'w')


li = gridfi.readline() # Skip system name
outfi_chg.write(li)
outfi_mag.write(li)

# Read lattice scaling constant
li = gridfi.readline()
outfi_chg.write(li)
outfi_mag.write(li)
li = li.split()
scale = zeros((3),float)
if len(li) == 1:
    li = float(li[0])
    for i in range(3):
        scale[i] = li
else:
    if len(li) == 3:
        for i in range(3):
            scale[i] = float(li[i])

# Read lattice vectors
latcons = zeros((3,3),float)
for i in range(3):
    li = gridfi.readline()
    outfi_chg.write(li)
    outfi_mag.write(li)
    li = li.split()
    for j in range(3):
        latcons[i,j] = float(li[j])*scale[j]

print latcons

# Is this lattice orthorhombic in z direction?
assert latcons[0,2] <= 1.0e-8
assert latcons[1,2] <= 1.0e-8
assert latcons[2,0] <= 1.0e-8
assert latcons[2,1] <= 1.0e-8

# Calculate volume
volume = vdot(latcons[0], cross(latcons[1],latcons[2]))
print "volume is ",volume,"ang^3"

# Read number of atoms
# Is this from vasp5 or vasp4? vasp5 has element names on the sixth line
# while vasp 4 does not.
li = gridfi.readline()
outfi_chg.write(li)
outfi_mag.write(li)
li = li.split()
if re.match("[0-9]",li[0].strip()):
    # It's vasp4
    nspecs = len(li)
    natoms = 0
    for i in range(nspecs):
        li[i] = int(li[i])
        natoms = natoms + li[i]
else:
    # It's vasp5. Read one more line.
    li = gridfi.readline()
    outfi_chg.write(li)
    outfi_mag.write(li)
    li = li.split()
    nspecs = len(li)
    natoms = 0
    for i in range(nspecs):
        li[i] = int(li[i])
        natoms = natoms + li[i]

print "Number of atoms:",natoms

li = gridfi.readline() # Skip one line. It probably says "Direct".
outfi_chg.write(li)
outfi_mag.write(li)
for i in range(natoms+1):
    li = gridfi.readline() # Skip the atom coordinates plus 1 blank line
    outfi_chg.write(li)
    outfi_mag.write(li)
# Read the grid dimensions
li = gridfi.readline()
outfi_chg.write(li)
outfi_mag.write(li)
grid = li.split()
for i in range(len(grid)):
    grid[i]=int(grid[i])
ngrid = grid[0] * grid[1] * grid[2]
dx = latcons[0,0]/grid[0]

# Now read the rest of the file
data=gridfi.read().split()
for i in range(ngrid):
    data[i]=float(data[i])

data_chg = data[0:ngrid]
data_mag = data[ngrid+3:]


for i in range(ngrid):
    outfi_chg.write(str(data_chg[i])+'\t')
    outfi_mag.write(str(data_mag[i])+'\t')
    if i % 10 == 9:
        outfi_chg.write('\n')
        outfi_mag.write('\n')




print len(data), ngrid
