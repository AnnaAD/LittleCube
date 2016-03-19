#! /usr/bin/env python

from Tkinter import *
from types import *
import math, random, time, sys, os, tempfile, copy
from optparse import OptionParser
import subprocess

#
# Basics of the program
#

WINDOW_WIDTH_IPHONE5  = 568
WINDOW_HEIGHT_IPHONE5 = 320


# 
# Safely delete an item from the canvas (if it exists)
# - assumes that deleted items are set to -1
# - generally used by setting the item to the return value here
# 
def SafeDelete(canvas, item):
    if item != -1:
        canvas.delete(item)
    return 

# called when something is horribly wrong
def Abort(str):
    print 'ABORTING [%s]' % str
    exit(1)


class Level:
    def __init__(self):
        self.number  = -1
        self.text    = ''
        self.boxes   = {}
        self.maxID   = 0

        self.boxMark = '__box__';
        self.txtMark = '__text__';
        return

    def SetNumber(self, number):
        self.number = number
        return

    def SetText(self, text):
        self.text = text
        return

    def GetText(self):
        return self.text

    def AddBox(self, x1, y1, x2, y2, mode):
        if x1 > x2:
            tmp = x1
            x1  = x2
            x2 = tmp
        if y1 > y2:
            tmp = y1
            y1  = y2
            y2 = tmp
        uid = self.maxID
        self.maxID += 1
        self.boxes[uid] = {'x1':x1, 'y1':y1, 'x2':x2, 'y2':y2, 'mode':mode, 'uid':uid}
        return uid

    def Length(self):
        return len(self.boxes)

    def GetBox(self, tid):
        assert(tid in self.boxes)
        return self.boxes[tid]

    def DeleteBox(self, tid):
        assert(tid in self.boxes)
        self.boxes[tid] = {'x1': -1, 'y1': -1, 'x2': -1, 'y2': -1, 'mode': -1, 'uid': -1}

    def PrintBoxes(self):
        print '\nBoxes:'
        for i in range(len(self.boxes)):
            print i, self.boxes[i]
        print ''

    def Load(self, outDir, level):
        fname = outDir + '/' + str(level)
        self.text = ''
        if os.path.isfile(fname):
            print 'Level: Load (%s)' % fname
            tmpBox = []
            fd = open(fname)
            for line in fd:
                tmp = line.split()
                if tmp[0] == self.boxMark:
                    x1, y1, x2, y2, mode = int(tmp[1]), int(tmp[2]), int(tmp[3]), int(tmp[4]), int(tmp[5])
                    tmpBox.append({'x1':x1, 'y1':y1, 'x2':x2, 'y2':y2, 'mode':mode})
                elif tmp[0] == self.txtMark:
                    self.text = line.strip()[len(self.txtMark)+1:]
                else:
                    print 'Level: malformed line, skipping (bad line %s)' % line.strip()
            fd.close()

            # now, read it all in, so populate
            self.maxID = 0
            self.boxes = {}
            for i in range(len(tmpBox)):
                self.boxes[i] = {'x1':tmpBox[i]['x1'], 'y1':tmpBox[i]['y1'], 'x2':tmpBox[i]['x2'], 'y2':tmpBox[i]['y2'],
                                 'mode':tmpBox[i]['mode'], 'uid':self.maxID}
                self.maxID += 1
        else:
            print 'Level: cannot find file %s, assuming this is a new level' % fname

    def Save(self, outDir, level):
        fname = outDir + '/' + str(level)
        fd = open(fname, 'w')
        outStr = '%s %s\n' % (self.txtMark, self.text)
        fd.write(outStr)
        for i in range(len(self.boxes)):
            b = self.boxes[i]
            if b['uid'] != -1:
                outStr = '%s %3d %3d %3d %3d %3d\n' % (self.boxMark, b['x1'], b['y1'], b['x2'], b['y2'], b['mode'])
                fd.write(outStr)
        fd.close()
        print 'Level: Save (%s)' % fname

# helper functions for buttons
def Update():
    global Ctrl
    Ctrl.DoUpdate()

def ModeZero():
    global Ctrl
    Ctrl.ModeZero()

def ModeOne():
    global Ctrl
    Ctrl.ModeOne()

def ModeTwo():
    global Ctrl
    Ctrl.ModeTwo()

def ModeThree():
    global Ctrl
    Ctrl.ModeThree()

def LevelUp():
    global Ctrl
    Ctrl.LevelUp()

def LevelDown():
    global Ctrl
    Ctrl.LevelDown()

def LevelInsert():
    global Ctrl
    Ctrl.LevelInsert()

def LevelDelete():
    global Ctrl
    Ctrl.LevelDelete()

def LevelGenerate():
    global Ctrl
    Ctrl.LevelGenerate()

def LevelDebug():
    global Ctrl
    Ctrl.LevelDebug()

#
# main work is done in this class
#
class Controller:
    def DoUpdate(self):
        self.levelName = self.e1.get()
        self.UpdateLevelText(self.levelName)
        self.level.SetText(self.levelName)
        self.level.Save(self.outDir, self.levelNumber)
        self.entryVariable.set('')
    
    def __init__(self, outDir):
        self.outDir = outDir

        # make the GUI
        self.root = Tk()
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH_IPHONE5, height=WINDOW_HEIGHT_IPHONE5)
        self.canvas.pack()

        self.f1 = Frame(height=1)
        self.f1.pack(fill=X)

        self.l1 = Label(self.root, text='Text', width=10)
        self.l1.pack(side=LEFT, in_=self.f1)

        self.entryVariable = StringVar()
        self.e1 = Entry(self.root, width=39, textvariable=self.entryVariable)
        self.e1.pack(side=LEFT, in_=self.f1)
        self.b1 = Button(self.root, text='Update', command=Update, width=10)
        self.b1.pack(side=LEFT, in_=self.f1)

        self.f2 = Frame(height=1)
        self.f2.pack(fill=X)

        self.l2 = Label(self.root, text='Modes', width=10)
        self.l2.pack(side=LEFT, in_=self.f2)
        self.m1 = Button(self.root, text='Normal (0)', command=ModeZero, width=10)
        self.m1.pack(side=LEFT, in_=self.f2)
        self.m2 = Button(self.root, text='Death (1)', command=ModeOne, width=10)
        self.m2.pack(side=LEFT, in_=self.f2)
        self.m3 = Button(self.root, text='Bouncy (2)', command=ModeTwo, width=10)
        self.m3.pack(side=LEFT, in_=self.f2)
        self.m4 = Button(self.root, text='Ice (3)', command=ModeThree, width=10)
        self.m4.pack(side=LEFT, in_=self.f2)

        self.f3 = Frame(height=1)
        self.f3.pack(fill=X)
        
        self.i0 = Label(self.root, text='Levels', width=10)
        self.i0.pack(side=LEFT, in_=self.f3)
        self.i2 = Button(self.root, text='-', command=LevelDown, width=10)
        self.i2.pack(side=LEFT, in_=self.f3)
        self.i1 = Button(self.root, text='+', command=LevelUp, width=10)
        self.i1.pack(side=LEFT, in_=self.f3)

        self.i3 = Button(self.root, text='Insert', command=LevelInsert, width=10)
        self.i3.pack(side=LEFT, in_=self.f3)
        self.i4 = Button(self.root, text='Delete', command=LevelDelete, width=10)
        self.i4.pack(side=LEFT, in_=self.f3)

        self.f4 = Frame(height=1)
        self.f4.pack(fill=X)

        self.j0 = Label(self.root, text='Code', width=10)
        self.j0.pack(side=LEFT, in_=self.f4)
        self.j1 = Button(self.root, text='Generate', command=LevelGenerate, width=24)
        self.j1.pack(side=LEFT, in_=self.f4)
        self.j2 = Button(self.root, text='Debug', command=LevelDebug, width=24)
        self.j2.pack(side=LEFT, in_=self.f4)
        
        # mouse buttons: they are complicated and hence ...
        self.canvas.bind('<ButtonPress-1>',         self.DrawBox)
        self.canvas.bind('<ButtonPress-2>',         self.KeyDeleteBox)
        self.canvas.bind('<Motion>',                self.UpdateMouse)
        self.root.bind('<Escape>',                  self.StopDrawingBox)

        # basic drawing stuff
        self.boxMode    = 0       # which type of box to draw: black, red, purple
        self.boxID      = -1      # used for the ID of the currently-drawn box
        self.boxNumToID = {}      # maps box numbers to canvas IDs
        self.hiliteBox  = -1      # if hovering over a box, this is its number (not canvas ID)
        
        # Fixed boxes
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH_IPHONE5, WINDOW_HEIGHT_IPHONE5, fill='gray',  outline='')
        self.canvas.create_rectangle(0, WINDOW_HEIGHT_IPHONE5 - 100, WINDOW_WIDTH_IPHONE5, WINDOW_HEIGHT_IPHONE5, fill='black', outline='')
        self.canvas.create_rectangle(0, 0, 20, WINDOW_HEIGHT_IPHONE5, fill='black', outline='')

        # don't forget guy himself
        self.canvas.create_rectangle(30, WINDOW_HEIGHT_IPHONE5 - 100 - 16, 46, WINDOW_HEIGHT_IPHONE5 - 100, fill='yellow',  outline='')

        # assumes nothing to start with
        self.levelNumber = 0       
        self.DrawLevelNumber()

        self.level       = Level()
        self.level.Load(self.outDir, self.levelNumber)
        self.level.PrintBoxes()

        self.levelName   = self.level.GetText()
        self.DrawLevelText()

        # draw boxes if they exist
        self.DrawLevel()

        # mode: either just moving the mouse, or drawing a box
        self.MODE_NIL   = 1
        self.MODE_DEF   = 2
        self.mode       = self.MODE_NIL
        self.DrawMode()

        # where is the mouse?
        self.mouseX     = 0
        self.mouseY     = 0
        self.DrawMousePosition()

        self.xmax = WINDOW_WIDTH_IPHONE5
        self.ymax = WINDOW_HEIGHT_IPHONE5

        # get it all going
        return

    def GetRoot(self):
        return self.root        

    #
    #
    #
    def DrawLevelNumber(self):
        self.levelTxt = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 80, text='Level : %3d' % self.levelNumber,
                                                font=('courier', 14), fill='white', anchor='w')
        return

    def UpdateLevelNumber(self):
        SafeDelete(self.canvas, self.levelTxt)
        self.DrawLevelNumber()
        return

    def DrawLevelText(self):
        self.nameID = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 60,  text='Text  : %s' % self.levelName,
                                              font=('courier', 14), fill='white', anchor='w')
        return

    def UpdateLevelText(self, name=''):
        self.levelName = name
        SafeDelete(self.canvas, self.nameID)
        self.DrawLevelText()
        return

    def DrawMode(self):
        self.modeTxt = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 40,  text='Mode  : %3d' % self.boxMode,
                                               font=('courier', 14), fill='white', anchor='w')
        return
    
    def DrawMousePosition(self):
        if self.mode == self.MODE_NIL:
            self.mouseTxt = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 20, text='Mouse : %3d,%3d' % (self.mouseX, self.mouseY),
                                                    font=('courier', 14), fill='white', anchor='w')
        else:
            self.mouseTxt = self.canvas.create_text(20, WINDOW_HEIGHT_IPHONE5 - 20, text='Mouse : %3d,%3d (%3d, %3d)' % (self.mouseX, self.mouseY, int(math.fabs(self.mouseX - self.startX)), int(math.fabs(self.mouseY - self.startY))),
                                                    font=('courier', 14), fill='white', anchor='w')
        return

    # helper function; really should just be a dict
    def GetColorFromMode(self, mode):
        if mode == 0:
            return 'black'
        elif mode == 1:
            return 'red'
        elif mode == 2:
            return 'purple'
        elif mode == 3:
            return 'lightblue'
        return

    # use this while defining a new box
    def CurrentBox(self):
        boxColor = self.GetColorFromMode(self.boxMode)
        if self.mode == self.MODE_DEF:
            self.boxID = self.canvas.create_rectangle(self.startX, self.startY, self.mouseX, self.mouseY, fill=boxColor, outline='')

    # use this when the mouse is moving
    def UpdateMouse(self, event):
        self.mouseX = event.x
        self.mouseY = event.y

        # show the current mouse position at all times
        SafeDelete(self.canvas, self.mouseTxt)
        self.DrawMousePosition()

        # also draw the current box if need be
        SafeDelete(self.canvas, self.boxID)
        self.CurrentBox()

        # if not defining a new box, check for hilight possibility
        if self.mode == self.MODE_NIL:
            self.hiliteBox = -1
            # clear all highlights
            for i in range(self.level.Length()):
                boxID = self.boxNumToID[i]
                self.canvas.itemconfig(boxID, outline='black', width=0)

            # find EXACTLY ONE to highlight
            max = self.level.Length()
            for i in range(max):
                j = max - i - 1
                box   = self.level.GetBox(j)
                if box['uid'] == -1:
                    continue
                boxID = self.boxNumToID[j]
                if self.mouseX < box['x2'] and self.mouseX > box['x1'] and self.mouseY < box['y2'] and self.mouseY > box['y1']:
                    self.canvas.itemconfig(boxID, outline='orange', width=2)
                    self.hiliteBox = j
                    break
                else:
                    self.canvas.itemconfig(boxID, outline='black', width=0)
        return

    # draws each box
    # also sets map of boxNums to canvasIDs
    def DrawLevel(self):
        self.boxNumToID = {}
        for i in range(self.level.Length()):
            b = self.level.GetBox(i)
            color = self.GetColorFromMode(b['mode'])
            tmpID = self.canvas.create_rectangle(b['x1'], b['y1'], b['x2'], b['y2'], fill=color, outline='', width=0)
            self.boxNumToID[i] = tmpID
        return

    # deletes each box
    # also unsets boxNum to canvasID map
    def UndrawLevel(self):
        for i in range(self.level.Length()):
            tmpID = self.boxNumToID[i]
            SafeDelete(self.canvas, tmpID)
        self.boxNumToID = {}
        return

    # call this when box being drawn right now is not the right one
    def StopDrawingBox(self, event):
        self.mode = self.MODE_NIL
        SafeDelete(self.canvas, self.boxID)
        return

    # first time click  : start drawing box
    # second time click : finish drawing box
    def DrawBox(self, event):
        # check if in range
        if event.y < 0 or event.y > self.ymax:
            return
        if event.x < 0 or event.x > self.xmax:
            return
        
        if self.mode == self.MODE_NIL:
            self.mode = self.MODE_DEF
            self.startX, self.startY = self.mouseX, self.mouseY
        elif self.mode == self.MODE_DEF:
            self.mode = self.MODE_NIL

            # draw the box
            boxColor = self.GetColorFromMode(self.boxMode)
            boxID    = self.canvas.create_rectangle(self.startX, self.startY, self.mouseX, self.mouseY, fill=boxColor, outline='')

            # add to current level
            bnum      = self.level.AddBox(self.startX, self.startY, self.mouseX, self.mouseY, self.boxMode)

            # record mapping of box number to this box's canvas ID
            self.boxNumToID[bnum] = boxID

            # save level to disk, print for no particular reason
            self.level.PrintBoxes()
            self.level.Save(self.outDir, self.levelNumber)
        return

    # unused: can bind this to a button if you like though
    def LevelSave(self):
        self.level.Save(self.outDir, self.levelNumber)
        return

    def LevelGenerate(self):
        # first we generate from the local format into .js
        process = subprocess.Popen('./generate.csh %s all > levels.js' % self.outDir, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert(str(process.returncode) == '0')

        # now we run one more script to stitch together final javascript stuff
        process = subprocess.Popen('./stitch.csh %s' % self.outDir, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert(str(process.returncode) == '0')
        return

    def LevelDebug(self):
        # first we generate from the local format into .js
        process = subprocess.Popen('./generate.csh %s %d > levels.js' % (self.outDir, self.levelNumber), shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert(str(process.returncode) == '0')

        # now we run one more script to stitch together final javascript stuff
        process = subprocess.Popen('./stitch.csh %s' % self.outDir, shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert(str(process.returncode) == '0')
        return

    def LevelInsert(self):
        # first we use the insert.csh script to make room for the new level
        # e.g., 'insert.csh outDir/ 3' will keep files 0, 1, 2, but move 4 to 5, 3 to 4, etc.
        process = subprocess.Popen('./insert.csh %s %d' % (self.outDir, self.levelNumber), shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert(str(process.returncode) == '0')
        self.UndrawLevel()

        # now we just make a blank level, which is enough for now
        # user actions (such as drawing) will populate it
        self.level = Level()
        self.UpdateLevelText('')
        self.level.PrintBoxes()
        return

    def LevelDelete(self):
        # first we use the delete.csh script to remove the level file and shift the others above it down
        # e.g., 'delete.csh outDir/ 3' will keep files 0, 1, 2, but move 4 to 3, 5 to 4, etc.
        process = subprocess.Popen('./delete.csh %s %d' % (self.outDir, self.levelNumber), shell=True, stdout=subprocess.PIPE)
        process.wait()
        assert(str(process.returncode) == '0')
        self.UndrawLevel()

        # now we create a new level object and fill it
        self.level = Level()
        self.level.Load(self.outDir, self.levelNumber)
        self.DrawLevel()
        self.UpdateLevelText(self.level.GetText())
        self.level.PrintBoxes()
        return

    def LevelUp(self):
        # save current level to disk, delete its boxes
        self.level.Save(self.outDir, self.levelNumber)
        self.UndrawLevel()

        # up the number on the screen
        self.levelNumber += 1
        self.UpdateLevelNumber()

        # create new level object (deleting the old) and load it
        self.level = Level()   
        self.level.Load(self.outDir, self.levelNumber)
        self.DrawLevel()
        self.UpdateLevelText(self.level.GetText())
        self.level.PrintBoxes()
        return

    def LevelDown(self):
        # can go up forever, but can't go down below 0
        if self.levelNumber == 0:
            return

        # save current, delete its boxes from screen
        self.level.Save(self.outDir, self.levelNumber)
        self.UndrawLevel()

        # down the screen number
        self.levelNumber -= 1
        self.UpdateLevelNumber()

        # create new level object (deleting old) and load it
        self.level = Level()   
        self.level.Load(self.outDir, self.levelNumber)
        self.DrawLevel()
        self.UpdateLevelText(self.level.GetText())
        self.level.PrintBoxes()
        return

    def KeyDeleteBox(self, event):
        if self.hiliteBox == -1:
            return
        self.level.DeleteBox(self.hiliteBox)
        SafeDelete(self.canvas, self.boxNumToID[self.hiliteBox])
        self.level.Save(self.outDir, self.levelNumber)
        self.level.PrintBoxes()
        return

    def ModeZero(self):
        self.boxMode = 0
        SafeDelete(self.canvas, self.modeTxt)
        self.DrawMode()
        return

    def ModeOne(self):
        self.boxMode = 1
        SafeDelete(self.canvas, self.modeTxt)
        self.DrawMode()
        return

    def ModeTwo(self):
        self.boxMode = 2
        SafeDelete(self.canvas, self.modeTxt)
        self.DrawMode()
        return

    def ModeThree(self):
        self.boxMode = 3
        SafeDelete(self.canvas, self.modeTxt)
        self.DrawMode()
        return

#
# MAIN 
#
parser = OptionParser()
parser.add_option('-o', '--outdir', default='Levels', help='where to store levels', action='store', type='string', dest='outDir')
(options, args) = parser.parse_args()

outDir = options.outDir
if os.path.isdir(outDir) == False:
    print 'Warning: %s does not exist, creating' % outDir
    os.mkdir(outDir)

Ctrl = Controller(outDir=outDir)
root = Ctrl.GetRoot()
root.mainloop()



