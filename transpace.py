#
# Transspace V.2016.05
# by md1ce
__author__ = "md1ce"
__version__ = "2016.05"
#
# -- Visualisation of the local space --
#
# hold left mouse button to rotate
# mouse wheel to zoom
# check also the menu-options
#
# You will a text file called "stars0.txt" to start (any other file an be loaded later with menu)
# This file contains the stars information
# It looks like this (remove the "#", Ross 154 is the last line in example, but can be
# expanded as you wish):
#$------><------><------><------><------><------><------><------><------><------><------><------><------><------>
#$Name                   $Dist   $Class  $Mag    $ASC            $DEC            $Remark
#$-----------------------ly.lylylG5.5V   xx.xx   hh:mm:ss.sssssss-dd:'':"".""""""--------------------------------
#Sol                     0.      G2V     4.85    00:00:00         00:00:00.      8 Planets
#Proxima Centauri        4.2421  M5.5Ve  15.53   14:29:43.       -62:40:46.
#Alpha Centauri AB       4.365   G2V     4.38    14:39:36.5      -60:50:02.      B = K1V
#Barnards Star           5.963   M4.0Ve  13.22   17:57:48.5       04:41:36.
#Luhman 16 AB            6.59    L8      100.    10:49:15.57     -53:19:06.      B = T1
#WISE 0855-0714          7.2     Y       100.    08:55:10.83     -07:14:42.5
#Wolf 359                7.7825  M6.0V   16.55   10:56:29.2       07:00:53.
#Lalande 21185           8.2905  M2V     10.44   11:03:20.2       35:58:12.
#Sirius AB               8.5828  A1V     1.42    06:45:08.9      -16:42:58.      B = DA2
#Luyten 726-8 AB         8.728   M5.5V   15.4    01:39:01.3      -17:57:01.      B = M6V
#Ross 154                9.6813  M3.5V   13.07   18:49:49.4      -23:50:10.
#
#
try:
   from tkinter import *     # python 3
except ImportError:
   from Tkinter import *     # python 2
from math import *
import tkinter.simpledialog as tkd
import tkinter.filedialog as tkf

# read file
def read_file(starFile):
    global noOfStars
    global nameStar
    global distanceStar
    global classStar
    global magStar
    global ascStar
    global decStar
    #global xpositionStar
    #global ypositionStar
    #global zpositionStar
    global positionStar

    f = open(starFile,'r')
    out=f.readlines()

    nameStar = [0]*maxStars
    distanceStar = [0]*maxStars
    classStar = [0]*maxStars
    magStar = [0]*maxStars
    ascStar = [0]*maxStars
    decStar = [0]*maxStars
    #xpositionStar = [0]*maxStars
    #ypositionStar = [0]*maxStars
    #zpositionStar = [0]*maxStars
    positionStar  = [[0 for x in range(maxStars)] for x in range(3)]

    noOfStars=0

    #interpret information from file
    for line in out:
        #print (line)
        if (line[0:1] != "$"):
            nameStar[noOfStars] =  line[0:24]
            distanceStar[noOfStars] = float(line[24:32])
            classStar[noOfStars] = line[32:40]
            magStar[noOfStars] = float(line[40:48])
            ascStar[noOfStars] = float(line[48:50])*360./24.+float(line[51:53])/4.+float(line[54:64])/240.
            decStar[noOfStars] = 90.-float(line[64:67])+float(line[68:70])/60.+float(line[71:80])/3600.
            noOfStars = noOfStars+1

    f.close()

#print file content
def print_data():
    for i in range(noOfStars):
        print(nameStar[i])
        print(distanceStar[i]+0.)
        print(classStar[i])
        print(ascStar[i])
        print(decStar[i])

#compute cartesian star positions
def compute_position():
    for i in range(noOfStars):
        positionStar[0][i] = distanceStar[i] * sin(decStar[i]*3.141592654/180.) * cos(-ascStar[i]*3.141592654/180.)
        positionStar[1][i] = distanceStar[i] * sin(decStar[i]*3.141592654/180.) * sin(-ascStar[i]*3.141592654/180.)
        positionStar[2][i] = distanceStar[i] * cos(decStar[i]*3.141592654/180.)

#print cartesian star positions
def print_position():
    for i in range(noOfStars):
        #print(nameStar[i], " x=", xpositionStar[i], " y=", ypositionStar[i], " z=", zpositionStar[i])
        print(nameStar[i], " x=", positionStar[0][i], " y=", positionStar[1][i], " z=", positionStar[2][i])


def translate(x,y,dx,dy):
    """Translate vector(x,y) by (dx,dy)."""

    return x+dx, y+dy

# draw starfield
def drawStarfield(starField,fixField):
    w = canvas.winfo_width()/2
    h = canvas.winfo_height()/2
    min_wh = min(w,h)

    #print("w=",w," h=",h)
    canvas.delete(ALL) # delete all edges

    nv = len(starField[0])

    # draw all line shorter than maxjump
    for i in range(0,nv):
        for j in range(i+1,nv):
            interdistance=((starField[0][i]-starField[0][j])**2+
                           (starField[1][i]-starField[1][j])**2+
                           (starField[2][i]-starField[2][j])**2)**0.5
            if (max(distanceStar[i],distanceStar[j]) > sphereSize):
                interdistance = maxjump+100.
            if (max(magStar[i],magStar[j]) > minAbsMag):
                interdistance = maxjump+100.
            #print (nameStar[i]," to ",nameStar[j]," is ",interdistance,"ly")
            if (interdistance<maxjump):
                canvas.create_line(
                    translate(starField[0][i]*min_wh/scalefactor,starField[1][i]*min_wh/scalefactor,w,h),
                    translate(starField[0][j]*min_wh/scalefactor,starField[1][j]*min_wh/scalefactor,w,h),
                    fill = lineColor)

    # True north
    canvas.create_line(
                    translate(0.,0.,w,h),
                    translate(fixField[0][0]*min_wh,fixField[1][0]*min_wh,w,h),
                    fill = "blue", arrow = 'last')
    canvas.create_text(fixField[0][0]*min_wh+w+20,fixField[1][0]*min_wh+h-10,
                    text="True north", anchor="center", fill="blue")
    #x-y
    canvas.create_line(
                    translate(0.,0.,w,h),
                    translate(fixField[0][1]*min_wh,fixField[1][1]*min_wh,w,h),
                    fill = "blue", arrow = 'last')
    canvas.create_text(fixField[0][1]*min_wh+w+10,fixField[1][1]*min_wh+h-10,
                    text="0h", anchor="center", fill="blue")
    canvas.create_line(
                    translate(0.,0.,w,h),
                    translate(fixField[0][2]*min_wh,fixField[1][2]*min_wh,w,h),
                    fill = "blue", arrow = 'last')
    canvas.create_text(fixField[0][2]*min_wh+w+10,fixField[1][2]*min_wh+h-10,
                    text="6h", anchor="center", fill="blue")
    #Galactic center
    canvas.create_line(
                    translate(0.,0.,w,h),
                    translate(fixField[0][3]*min_wh,fixField[1][3]*min_wh,w,h),
                    fill = "red", arrow = 'last')
    canvas.create_text(fixField[0][3]*min_wh+w+20,fixField[1][3]*min_wh+h-10,
                    text="Galactic center", anchor="center", fill="red")
    #Galactic north
    canvas.create_line(
                    translate(0.,0.,w,h),
                    translate(fixField[0][4]*min_wh,fixField[1][4]*min_wh,w,h),
                    fill = "red", arrow = 'last')
    canvas.create_text(fixField[0][4]*min_wh+w+20,fixField[1][4]*min_wh+h-10,
                    text="Galactic north", anchor="center", fill="red")
    #equator
    for i in range (89):
        canvas.create_line(
                    translate(fixField[0][5+i]*min_wh,fixField[1][5+i]*min_wh,w,h),
                    translate(fixField[0][6+i]*min_wh,fixField[1][6+i]*min_wh,w,h),
                    fill = "blue", dash=(2,5))
    canvas.create_line(
                    translate(fixField[0][5+89]*min_wh,fixField[1][5+89]*min_wh,w,h),
                    translate(fixField[0][5]*min_wh,fixField[1][5]*min_wh,w,h),
                    fill = "blue", dash=(2,5))
    canvas.create_text(fixField[0][50]*min_wh+w+20,fixField[1][50]*min_wh+h-10,
                    text="Equator", anchor="center", fill="blue")

    # draw stars
    for i in range(0,nv):
        starColor = "green" # unknown star class
        if (classStar[i][0:1]=="O"):
            starColor = "blue"
        elif (classStar[i][0:1]=="B"):
            starColor = "sky blue"
        elif (classStar[i][0:1]=="A"):
            starColor = "white"
        elif (classStar[i][0:1]=="F"):
            starColor = "pale goldenrod"
        elif (classStar[i][0:1]=="G"):
            starColor = "yellow"
        elif (classStar[i][0:1]=="K"):
            starColor = "orange"
        elif (classStar[i][0:1]=="M"):
            starColor = "red"
        elif (classStar[i][0:1]=="L"):
            starColor = "firebrick"
        elif (classStar[i][0:1]=="T"):
            starColor = "brown"
        elif (classStar[i][0:1]=="Y"):
            starColor = "sienna"
        elif (classStar[i][0:1]=="D"):
            starColor = "black" # white dwarfs

        size = 3
        if (magStar[i]>20.):
            size = 2
        elif (magStar[i]<6.):
            size = 9-int(magStar[i])
        if (distanceStar[i] <= sphereSize):
            if (magStar[i] <= minAbsMag):
                canvas.create_oval(-size+starField[0][i]*min_wh/scalefactor+w,-size+starField[1][i]*min_wh/scalefactor+h,
                           size+starField[0][i]*min_wh/scalefactor+w , size+starField[1][i]*min_wh/scalefactor+h,
                           fill = starColor)
                canvas.create_text(starField[0][i]*min_wh/scalefactor+w+20,starField[1][i]*min_wh/scalefactor+h-10,
                           text=nameStar[i], anchor="center")

    canvas.create_text(20,30,text='Connections <' + str(maxjump) + 'ly' + "\n" +
                                   "Sphere radius =" + str(sphereSize) + "ly" + "\n" +
                                   "Zoom radius =" + str(scalefactor) + "ly" + "\n" +
                                   "Minimal absolute magnitude =" + str(minAbsMag), anchor="w")


def createZeroMat(m,n):
    """Return a matrix (m x n) filled with zeros."""

    ret = [0] * m
    for i in range(m):
        ret[i] = [0] * n
    return ret

def matMul(mat1, mat2):
    """Return mat1 x mat2 (mat1 multiplied by mat2)."""

    m = len(mat1)
    n = len(mat2[0])
    common = len(mat2)

    ret = createZeroMat(m,n)
    if  len(mat1[0]) == len(mat2):
      for i in range(m):
          for j in range(n):
              for k in range(common):
                  ret[i][j] += mat1[i][k] * mat2[k][j]
    return ret

def matTrans(mat):
    """Return mat (n x m) transposed (m x n)."""

    m = len(mat[0])
    n = len(mat)

    ret = createZeroMat(m,n)
    for i in range(m):
        for j in range(n):
            ret[i][j] = mat[j][i]
    return ret

# Initialize global variables
def init():

    global ROT_X, ROT_Y, ROT_Z
    global eps, EPS, starField, fixField
    global lastX, lastY, lineColor, bgColor
    global scalefactor, sphereSize

    starField = createZeroMat(3,noOfStars)
    fixField  = createZeroMat(3,95)

    scalefactor = max(distanceStar)
    sphereSize = scalefactor

    for j in range(noOfStars):
        for i in range(3):
            starField[i][j] = positionStar[i][j]

    # create fixed points
    #  True north
    fixField[0][0] = 0.
    fixField[1][0] = 0.
    fixField[2][0] = 1.
    #  x-y
    fixField[0][1] = 1
    fixField[1][1] = 0.
    fixField[2][1] = 0.
    fixField[0][2] = 0.
    fixField[1][2] = -1.
    fixField[2][2] = 0.
    #  galactic center
    fixField[0][3] = sin((90+28.94)*3.141592654/180.) * cos(-266.4*3.141592654/180.)
    fixField[1][3] = sin((90+28.94)*3.141592654/180.) * sin(-266.4*3.141592654/180.)
    fixField[2][3] = cos((90+28.94)*3.141592654/180.)
    #  galactic north
    fixField[0][4] = sin((90-27.13)*3.141592654/180.) * cos(-192.85*3.141592654/180.)
    fixField[1][4] = sin((90-27.13)*3.141592654/180.) * sin(-192.85*3.141592654/180.)
    fixField[2][4] = cos((90-27.13)*3.141592654/180.)
    #  ecliptic
    for i in range (90):
        fixField[0][5+i] = sin(90*3.141592654/180.) * cos(-(i-1)*4*3.141592654/180.)
        fixField[1][5+i] = sin(90*3.141592654/180.) * sin(-(i-1)*4*3.141592654/180.)
        fixField[2][5+i] = 0.

    # counter-clockwise rotation about the X axis
    ROT_X = lambda x: matTrans([[1,0,0],           [0,cos(x),-sin(x)], [0,sin(x),cos(x)] ])

    # counter-clockwise rotation about the Y axis
    ROT_Y = lambda y: matTrans([[cos(y),0,sin(y)], [0,1,0],            [-sin(y),0,cos(y)]])

    # counter-clockwise rotation about the Z axis
    ROT_Z = lambda z: matTrans([[cos(z),sin(z),0], [-sin(z),cos(z),0], [0,0,1]])

    eps = lambda d: pi/360 if (d>0) else -pi/360
    EPS = lambda d: d*pi/360

    lastX = 0
    lastY = 0
    lineColor = 'black'
    bgColor = 'white'

def cbClicked(event):
    """Save current mouse position."""

    global lastX, lastY

    lastX = event.x
    lastY = event.y

def cbMotion(event):
    """Map mouse displacements in Y direction to rotations about X axis,
       and mouse displacements in X direction to rotations about Y axis."""

    global starField, fixField

    # Y coordinate is upside down
    dx = lastY - event.y
    starField = matMul(ROT_X(EPS(-dx)),starField)

    dy = lastX - event.x
    starField = matMul(ROT_Y(EPS(dy)),starField)

    dx = lastY - event.y
    fixField = matMul(ROT_X(EPS(-dx)),fixField)

    dy = lastX - event.x
    fixField = matMul(ROT_Y(EPS(dy)),fixField)

    drawStarfield(starField,fixField)
    cbClicked(event)

def resize(event):
    """Redraw, in case of a window change due to user resizing it."""

    drawStarfield(starField,fixField)

# zoom
def wheelUp(event):

    global starField,scalefactor,fixField

    scalefactor=scalefactor+1

    drawStarfield(starField,fixField)

# zoom
def wheelDown(event):

    global starField,scalefactor,fixField
    scalefactor=scalefactor+1
    drawStarfield(starField,fixField)

# zoom
def wheel(event):

    global starField,scalefactor,fixField

    scalefactor=scalefactor+event.delta/4800*scalefactor
    drawStarfield(starField,fixField)

def load_starfile(file=None):
    file_name = tkf.askopenfilename(defaultextension='.txt',
                                   filetypes=(('star files', '*.txt'), ('All files', '*.*')))

    print ("File read: ",file_name)
    read_file(file_name)
    #print_data()
    compute_position()
    #print_position()

    init()

    drawStarfield(starField,fixField)

# set maxjump
def set_maxjump():
    global maxjump

    maxjump = tkd.askfloat('Max. distance', 'enter maximal distance for connection lines')

    drawStarfield(starField,fixField)

# set sphereSize
def set_sphereSize():
    global sphereSize,scalefactor

    sphereSize = tkd.askfloat('Star field size', 'enter maximal distance for center to farthest star')
    scalefactor = sphereSize

    drawStarfield(starField,fixField)

def set_minAbsMag():
    global sphereSize,scalefactor,minAbsMag

    minAbsMag = tkd.askfloat('Minimal absolute magnitude', 'enter minimal visible absolute magnitude (>100 to see all)')

    drawStarfield(starField,fixField)

# menu
def makemenu(win):
    top = Menu(win)  # win=top-level window
    win.config(menu=top)  # set its menu option
    filemenu = Menu(top)
    filemenu.add_command(label='Open...', command=load_starfile, underline=0)
    filemenu.add_command(label='Quit', command=sys.exit, underline=0)
    top.add_cascade(label='File', menu=filemenu, underline=0)
    edit = Menu(top, tearoff=False)
    edit.add_command(label='Set max. connection distance', command=set_maxjump, underline=0)
    edit.add_command(label='Set star field size', command=set_sphereSize, underline=0)
    edit.add_command(label='Minimal absolute magnitude', command=set_minAbsMag, underline=0)
    edit.add_separator()
    top.add_cascade(label='Edit', menu=edit, underline=0)

def main():
    global maxStars
    global maxjump,minAbsMag
    global file_name

    print ("Start TRANSSPACE")
    file_name="stars0.txt"
    maxStars=10000
    maxjump = 7.
    minAbsMag = 200.

    print ("File read: ",file_name)
    read_file(file_name)
    #print_data()
    compute_position()
    #print_position()

    global canvas
    root = Tk()
    root.title('Star Field')
    root.geometry('+0+0')

    init()

    makemenu(root)

    canvas = Canvas(root, width=1000, height=1000, background=bgColor)
    canvas.pack(fill=BOTH,expand=YES)
    canvas.bind("<Button-1>", cbClicked)
    canvas.bind("<B1-Motion>", cbMotion)
    canvas.bind("<Configure>", resize)

    from platform import uname
    os = uname()[0]
    if ( os == "Linux" ):
         canvas.bind('<Button-4>', wheelUp)      # X11
         canvas.bind('<Button-5>', wheelDown)
    elif ( os == "Darwin" ):
         canvas.bind('<MouseWheel>', wheel)      # MacOS
    else:
         canvas.bind_all('<MouseWheel>', wheel)  # windows

    drawStarfield(starField,fixField)

    mainloop()

if __name__=='__main__':
    sys.exit(main())