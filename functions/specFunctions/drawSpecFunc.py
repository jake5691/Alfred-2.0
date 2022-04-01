import requests
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
import matplotlib.pyplot as plt
from langdetect import detect


#Image size
x = 1024
y = x

x_center = x/2
y_center = y/2
radius = int((1-3/11)*y_center)

radiusDict_gr = {
  1:int((1-9.5/11)*y_center),
  2:int((1-8.5/11)*y_center),
  3:int((1-7.5/11)*y_center),
  4:int((1-6/11)*y_center),
  5:int((1-4.5/11)*y_center),
  6:int((1-3/11)*y_center),
  7:int((1-2/11)*y_center),
  8:int((1-1/11)*y_center),
  9:int((1-0/11)*y_center),
  10:int((1+1/11)*y_center),

}

radiusDict_bl = {
  1:int((1-9.6/11)*y_center),
  2:int((1-8.9/11)*y_center),
  3:int((1-8.2/11)*y_center),
  4:int((1-7.4/11)*y_center),
  5:int((1-6.6/11)*y_center),
  6:int((1-5.9/11)*y_center),
  7:int((1-5.1/11)*y_center),
  8:int((1-4.3/11)*y_center),
  9:int((1-3.6/11)*y_center),
  10:int((1-2.8/11)*y_center),
  11:int((1-2.0/11)*y_center),
  12:int((1-1.3/11)*y_center),
  13:int((1-0.5/11)*y_center),
}

radiusDict_red = {
  1:int((1-10/11)*y_center),
  2:int((1-9.5/11)*y_center),
  3:int((1-9.2/11)*y_center),
  4:int((1-8.7/11)*y_center),
  5:int((1-8.2/11)*y_center),
  6:int((1-7.4/11)*y_center),
  
  7:int((1-6.6/11)*y_center),
  8:int((1-6.1/11)*y_center),
  9:int((1-5.8/11)*y_center),
  10:int((1-5.3/11)*y_center),
  11:int((1-4.8/11)*y_center),
  12:int((1-4/11)*y_center),
  
  13:int((1-3.2/11)*y_center),
  14:int((1-2.7/11)*y_center),
  15:int((1-1.9/11)*y_center),
  16:int((1-1.2/11)*y_center),
  17:int((1-0.5/11)*y_center)
}

# Load font from URI
#truetype_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true'

truetype_url = 'https://github.com/googlefonts/noto-fonts/blob/main/hinted/ttf/NotoSans/NotoSans-Black.ttf?raw=true'
r = requests.get(truetype_url, allow_redirects=True)
font = ImageFont.truetype(io.BytesIO(r.content), size=24)


font_wm = ImageFont.truetype(io.BytesIO(r.content), size=42)

def getX_bl(angle:int,radius:int=6,offset_x:int=0):
  """Get X coordinate (rotated correctly)"""
  radiusDict = radiusDict_bl
  r = radiusDict[radius]
  angle = angle * np.deg2rad(15) - np.arctan(offset_x/r)
  radius = np.sqrt(r*r+offset_x*offset_x)
  x = np.sin(angle) * radius + x_center
  return x
  
def getY_bl(angle:int,radius:int=6,offset_x:int=0):
  """Get Y coordinate (rotated correctly)"""
  radiusDict = radiusDict_bl
  r = radiusDict[radius]
  angle = angle * np.deg2rad(15) - np.arctan(offset_x/r)
  radius = np.sqrt(r*r+offset_x*offset_x)
  y = np.cos(angle) * radius + y_center
  return y

def getPoint_bl(angle:int,radius:int=6,offset_x:int=0):
  """Get point (x,y)"""
  x = getX_bl(angle,radius,offset_x)
  y = getY_bl(angle,radius,offset_x)
  return (x,y)

def getX_gr(angle:int,radius:int=6,offset_x:int=0):
  """Get X coordinate (rotated correctly)"""
  radiusDict = radiusDict_gr
  r = radiusDict[radius]
  angle = angle * np.deg2rad(15) - np.arctan(offset_x/r)
  radius = np.sqrt(r*r+offset_x*offset_x)
  x = np.sin(angle) * radius + x_center
  return x
  
def getY_gr(angle:int,radius:int=6,offset_x:int=0):
  """Get Y coordinate (rotated correctly)"""
  radiusDict = radiusDict_gr
  r = radiusDict[radius]
  angle = angle * np.deg2rad(15) - np.arctan(offset_x/r)
  radius = np.sqrt(r*r+offset_x*offset_x)
  y = np.cos(angle) * radius + y_center
  return y

def getPoint_gr(angle:int,radius:int=6,offset_x:int=0):
  """Get point (x,y)"""
  x = getX_gr(angle,radius,offset_x)
  y = getY_gr(angle,radius,offset_x)
  return (x,y)

def getX_red(angle:int,radius:int=6,offset_x:int=0):
  """Get X coordinate (rotated correctly)"""
  radiusDict = radiusDict_red
  r = radiusDict[radius]
  angle = angle * np.deg2rad(15) - np.arctan(offset_x/r)
  radius = np.sqrt(r*r+offset_x*offset_x)
  x = np.sin(angle) * radius + x_center
  return x
  
def getY_red(angle:int,radius:int=6,offset_x:int=0):
  """Get Y coordinate (rotated correctly)"""
  radiusDict = radiusDict_red
  r = radiusDict[radius]
  angle = angle * np.deg2rad(15) - np.arctan(offset_x/r)
  radius = np.sqrt(r*r+offset_x*offset_x)
  y = np.cos(angle) * radius + y_center
  return y

def getPoint_red(angle:int,radius:int=6,offset_x:int=0):
  """Get point (x,y)"""
  x = getX_red(angle,radius,offset_x)
  y = getY_red(angle,radius,offset_x)
  return (x,y)



async def draw(groups, col1, col2, filename, firstSpecs, colour, author):
  try:
    language = detect(author.display_name)
  except:
    language = 'english'
 
  grey = (200,200,200)
  white = (255,255,255)
  print(filename)
  with Image.new("RGB",(x,y),color = (255,255,255)) as im:
    draw = ImageDraw.Draw(im)
    #Draw the connections
    for fiSpec in firstSpecs:
      draw.line(
            [(x_center, y_center), fiSpec.center],
            fill = grey,
            width = 3
          )
      fiSpec.activatable = True
      #Loop groups 
      for group in groups:
        start = None
        #Loop specs in group
        for s in group:
          #draw connecting line
          if start != None:
            draw.line(
              [start, s.center],
              fill = grey,
              width = 3
            )
            pass
          start = s.center
          
  #Draw the Center
  draw.ellipse(
    [x_center-30,
     y_center-30,
     x_center+30,
     y_center+30],
    outline = col1,
    fill = col1,
    width=3
    ) 

#Draw Specs
    #Loop groups 
  for group in groups:
    start = None
    precondition = False
      #Loop specs in group
    for s in group:
      if precondition:
        s.activatable = True
      fill_color = white
      if s.currentLvl  == s.maxLvl:
        fill_color = col1
      elif s.currentLvl > 0:
        fill_color = col2
        #Define the size of the circle
      
      if colour == "blue":
        if s.bigCircle:
          size = 18
        else: 
          size = 12
        tl = (s.center[0]-size,s.center[1]-size)
        br = (s.center[0]+size,s.center[1]+size)
        #draw the circle
        draw.ellipse(
          [tl,br],
          outline = col1,
          fill=fill_color,
          width=2
        )
      elif colour == "green":
        draw.ellipse(
          [s.topLeft,
           s.bottomRight],
          outline = col1,
          fill=fill_color,
          width=2
        )
      elif colour == "red":
        draw.ellipse(
          [s.topLeft,
           s.bottomRight],
          outline = col1,
          fill=fill_color,
          width=2
        )
        
        
      text = str(s.currentLvl) if s.currentLvl < s.maxLvl else str(s.maxLvl)
      if text == "0" and not(s.activatable):
        text = ""
      fill = grey if s.currentLvl == 0 else white
      draw.text(s.center, text=text, fill=fill, font=font, language=language, anchor="mm")
      if s.currentLvl == s.maxLvl:
        precondition = True
      else:
        precondition = False
      #add watermark
      draw.text((20, 20), "RbC - 232", 
          (0, 0, 0), font=font_wm)
      draw.text((20,80), author, 
          (0, 0, 0), font=font_wm)
      
  im.save(filename)



