import os
import pygame
from utils.loading              import loadImage, loadImageSize

class Character:
   
   DIR_SOUTH         = "south"
   DIR_NORTH         = "north"
   DIR_WEST          = "west"
   DIR_EAST          = "east"
   
   STATE_STANDING    = "standing"
   STATE_WALKING     = "walking"
   
   charWidth         = 32
   charHeight        = 48
   
   movingPositions   = []
   
   startpoint        = (0,0)
   endpoint          = (0,0)
   pathlines         = []
   
   # These describe where each 
   # character's different sprites
   # are located.
   south1            = (0,           0)
   south2            = (1*charWidth, 0)
   south3            = (2*charWidth, 0)
   
   west1             = (0,           1*charHeight)
   west2             = (1*charWidth, 1*charHeight)
   west3             = (2*charWidth, 1*charHeight)
   
   east1             = (0,           2*charHeight)
   east2             = (1*charWidth, 2*charHeight)
   east3             = (2*charWidth, 2*charHeight)
   
   north1            = (0,           3*charHeight)
   north2            = (1*charWidth, 3*charHeight)
   north3            = (2*charWidth, 3*charHeight)
   
   # distance to
   type1             = (0,0)
   type2             = (charWidth*3,0)
   type3             = (charWidth*6,0)
   type4             = (charWidth*9,0)
   
   type5             = (0,charHeight*4)
   type6             = (charWidth*3,charHeight*4)
   type7             = (charWidth*6,charHeight*4)
   type8             = (charWidth*9,charHeight*4)
   
   type              = None
   name              = 'no_name'
   tempTotalCapital  = 0
   
   state             = STATE_STANDING
   direction         = DIR_SOUTH
   x                 = 0
   y                 = 0
   picture           = os.path.join('resources','characters.png')
   animState         = 0
   curAnim           = None
   
   nametagSheet      = pygame.image.load(os.path.join('resources','nametag.png'))
   nametagImage      = None
   
   def __init__(self):
      self.movingPositions = []
      self.nametagImage = loadImageSize(self.nametagSheet,
                                 0,
                                 0,
                                 97,
                                 43
                                )
   
   def setMovingPositions(this,mp):
      this.movingPositions = mp
   
   def getOffset(this):
      
      offset = (0,0)
      
      if this.movingPositions and len(this.movingPositions) > 0:
         
         this.state = this.STATE_WALKING
         
         if this.x == this.movingPositions[0][0] and this.y == this.movingPositions[0][1]:
            if len(this.movingPositions)>0:
               this.movingPositions.pop(0)
         
         if len(this.movingPositions)>0:
            if this.x < this.movingPositions[0][0]:
               this.x += 4
               this.setDir(this.DIR_EAST)
            elif this.x > this.movingPositions[0][0]:
               this.x -= 4
               this.setDir(this.DIR_WEST)
         
            if this.y < this.movingPositions[0][1]:
               this.y += 4
               this.setDir(this.DIR_SOUTH)
            elif this.y > this.movingPositions[0][1]:
               this.y -= 4
               this.setDir(this.DIR_NORTH)
      else:
         this.state = this.STATE_STANDING
         
      if   this.state == this.STATE_STANDING:
         if   this.direction == this.DIR_SOUTH:
            offset = (this.type[0]+this.south2[0],this.type[1]+this.south2[1])
         elif this.direction == this.DIR_NORTH:
            offset = (this.type[0]+this.north2[0],this.type[1]+this.north2[1])
         elif this.direction == this.DIR_WEST:
            offset = (this.type[0]+this.west2[0],this.type[1]+this.west2[1])
         elif this.direction == this.DIR_EAST:
            offset = (this.type[0]+this.east2[0],this.type[1]+this.east2[1])
            
      elif this.state == this.STATE_WALKING:
         
         if this.animState == 0:
            if   this.direction == this.DIR_SOUTH:
               this.curAnim = this.south3
            elif this.direction == this.DIR_NORTH:
               this.curAnim = this.north3
            elif this.direction == this.DIR_WEST:
               this.curAnim = this.west3
            elif this.direction == this.DIR_EAST:
               this.curAnim = this.east3
         elif this.animState == 1:
            if   this.direction == this.DIR_SOUTH:
               this.curAnim = this.south2
            elif this.direction == this.DIR_NORTH:
               this.curAnim = this.north2
            elif this.direction == this.DIR_WEST:
               this.curAnim = this.west2
            elif this.direction == this.DIR_EAST:
               this.curAnim = this.east2
         elif this.animState == 2:
            if   this.direction == this.DIR_SOUTH:
               this.curAnim = this.south1
            elif this.direction == this.DIR_NORTH:
               this.curAnim = this.north1
            elif this.direction == this.DIR_WEST:
               this.curAnim = this.west1
            elif this.direction == this.DIR_EAST:
               this.curAnim = this.east1
         
         if this.animState < 3:
            this.animState += 0.5
         else:
            this.animState = 0
         
         offset = (this.type[0]+this.curAnim[0],this.type[1]+this.curAnim[1])
         
      return offset
   
   def width(this):
      return this._width
   
   def offset(this):
      return this.sprite_initial_offset
      
   def setOffset(this,off):
      this.sprite_initial_offset = off
      
   def dist(this):
      return this.sprite_distance
      
   def setDir(this,dire):
      this.direction = dire
            
   def pic(this):
      return this.picture
   
   def setType(this,type):
      this.type = type
      
   def setName(this,name):
      this.name = name
      
   def setTempTotalCapital(this,tempTotalCapital):
      this.tempTotalCapital = tempTotalCapital