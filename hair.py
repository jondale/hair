import opc
import time
from PIL import Image, ImageDraw, ImageFont

HAIR_SIM = True

class HairyPixels:
    width = 0
    height = 0
    _PIXELS = []

    def __init__ (self,width=None,height=None,filename=None,image=None,default_pixel=None):
        self._PIXELS=[]
        if filename or image:
            self.load_image(width=width,height=height,filename=filename,image=image)
        elif width != None and height != None:
            self.width = width
            self.height = height
            self._PIXELS = [default_pixel,] * (self.width * self.height)

    def __eq__(self,other):   
        return self._PIXELS == other
    def __getitem__(self,key):
        x,y = key
        return self.get_pixel(x,y)
    
    def __setitem__(self,key,val):
        x,y = key
        self.set_pixel(x,y,val)
    
    def __len__(self):
        return len(self._PIXELS)
       
    def __add__(self,other):
        return self.add(other)
    
    def copy(self,obj):
        self.width = int(obj.width)
        self.height = int(obj.height)
        self._PIXELS = list(obj._PIXELS)

    def get_raw(self):
        pixels = [(0,0,0) if p==None else p[:3] for p in list(self._PIXELS)]
        return pixels
                    
    def load_image(self,width=None,height=None,filename=None,image=None):
        if filename:
            img = Image.open(filename)
        else:
            img = image
        img = img.convert("RGBA")
        if width and not height:
            old_width, old_height = img.size
            ratio = float(old_width) / float(old_height)
            height = int(width / ratio)
        elif height and not width:
            old_width, old_height = img.size
            ratio = float(old_width) / float(old_height)
            width = int(height * ratio)
        if width and height:
            img = img.resize((width,height),Image.ANTIALIAS)
        self.width, self.height = img.size
        self._PIXELS = [None,] * (self.width * self.height)
        img2 = Image.new("RGBA",img.size,(0,0,0))
        img2.paste(img)
        img = img2
        pixels = img.load()
        for y in xrange(self.height):
            for x in xrange(self.width):
                pixel = list(pixels[x,y])
                try:
                    self.set_pixel(x,y,pixel)
                except:
                    pass
        
    def load_text(self,text,width=None,height=None,color=(255,255,255),ttf=None):
        img = Image.new("RGBA",(1000,200), (0,0,0))
        draw = ImageDraw.Draw(img)
        if ttf==None:
            font = ImageFont.load_default()
        else:
            font = ImageFont.truetype(ttf,100)

        size = draw.textsize(text, font=font)
        w,h = size
        if width==None:
            width = int(w * (float(height)/h))
        img = Image.new("RGBA",size,(0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.text((0,0), text, color, font=font )
        
        # The below silliness is because bbox does not work well with truetype fonts.
        w,h = img.size
        x1 = int(w)
        y1 = int(h)
        x2 = 0
        y2 = 0
        for y in xrange(h):
            for x in xrange(w):
                alpha = img.getpixel((x,y))[3]
                if alpha > 0:
                    x1 = min(x1,x)
                    x2 = max(x2,x)
                    y1 = min(y1,y)
                    y2 = max(y1,y)
        x2 = min(w,x2+1)
        y2 = min(h,y2+1)
        img = img.crop((x1,y1,x2,y2))
        self.load_image(width=width, height=height, image=img)
        return self
    
    def add(self,other):
        # Adding a HairyPixel concatenates it to the right side.
        new_width = self.width + other.width
        new_height = max(self.height,other.height)
        new_pixels = HairyPixels(new_width, new_height)
        new_pixels.overlay(self,0,0)
        new_pixels.overlay(other,self.width,new_height)
        return new_pixels
    
    def get_coord(self,x,y):
        k = len(self._PIXELS) - ( (y * self.width ) + (self.width -  x) )
        #print "%d,%d = %d" % (x,y,k)
        return int(k)
    
    def get_pixel(self,x,y):
        try:
            return self._PIXELS[self.get_coord(x,y)]
        except:
            return None

    def set_pixel(self,x,y,pixel):
        if x>=0 and x<self.width and y>=0 and y<self.height:
            self._PIXELS[self.get_coord(x, y)] = pixel

    def blend_pixel(self, pixel1, pixel2):
        if pixel2 == None:
            return pixel1
        try:
            alpha = (pixel2[3] / 255.0)
            r1, g1, b1 = pixel1[:3]
            r2, g2, b2 = pixel2[:3]
            r = ( r2 * alpha ) + ( r1 * ( 1.0 - alpha ) )
            g = ( g2 * alpha ) + ( g1 * ( 1.0 - alpha ) )
            b = ( b2 * alpha ) + ( b1 * ( 1.0 - alpha ) )
            return (r,g,b)
        except:
            return pixel2

    def flip_horizontal(self):
        for y in range(self.height):
            for x in range(self.width/2):
                left = self.get_pixel(x,y)
                right = self.get_pixel(self.width-1-x,y)
                self.set_pixel(self.width - 1 - x, y, left)
                self.set_pixel(x, y, right)        
                
    def overlay (self, pixels, x=0, y=0):
        if not pixels:
            return None
        x = int(x)
        y = int(y)
        x1_min = int(max(0,x))
        x1_max = int(min(self.width,x+pixels.width))
        y1_min = int(max(0,y))
        y1_max = int(min(self.height,y+pixels.height))

        for y1 in xrange(y1_min,y1_max):
            y2 = y1 - y
            for x1 in xrange(x1_min,x1_max):
                x2 = x1 - x
                self.set_pixel(x1,y1,self.blend_pixel(self[x1,y1],pixels[x2,y2]))
                
#############################################################################        
                
class HairyBuffer:
    _BUFFER = []
    buffer_step = -1
    start_time = None
    end_time = None
    active = True
    visible = True
    repeat = True
    x = 0
    y = 0
    target_path = []
    target_x = None
    target_y = None
    target_step = None
    target_delay = None
    FPS = 0
    last_frame_time = None
    last_update_time = None
    
    def __init__(self,x=0,y=0):
        self._BUFFER = []
        self.buffer_step = -1
        self.start_time = None
        self.end_time = None
        self.active = True
        self.visible = True
        self.x = x
        self.y = y
        self.target_path = []
        self.target_x = None
        self.target_y = None
        self.target_step = None
        self.target_delay = None
        self.repeat = True
        self.FPS = 0
        self.last_frame_time = None
        self.last_update_time = None
        
    def __getitem__(self,key):
        return self._BUFFER[key]

    def __len__(self):
        return len(self._BUFFER)
    
    def __add__(self,other):
        return self.add(other)

    def add_sprite(self,filename=None,width=None,height=None,x1=None,y1=None,x2=None,y2=None,image=None):
        if filename:
            image = Image.open(filename)
        image.convert("RGBA")
        sprite = image.crop([x1,y1,x2,y2])
        return self.add_image(image=sprite,width=width,height=height)
        
    def add_gif(self,filename=None,image=None,width=None,height=None):
        if filename:
            image = Image.open(filename)
        gif = image
        while gif:
            try:
                frame = HairyPixels(image=gif,width=width,height=height)
                self.add(frame)
                gif.seek( gif.tell()+1 )
            except EOFError:
                gif.seek(0)
                break
        return self
    
    def add_image(self,filename=None,width=None,height=None,image=None):
        if filename:
            pixels = HairyPixels(filename=filename,width=width,height=height)
        else:
            pixels = HairyPixels(image=image,width=width,height=height)
        self.add(pixels)
        return self
        
    
    def add_text(self,text,width=None,height=None,color=(255,255,255),ttf=None):
        pixels = HairyPixels()
        pixels.load_text(text=text, width=width, height=height, color=color,ttf=ttf)
        self.add(pixels)
        return self
        #img = Image.new("RGBA",(1000,200), (0,0,0))
        #draw = ImageDraw.Draw(img)
        #if ttf==None:
            #font = ImageFont.load_default()
        #else:
            #font = ImageFont.truetype(ttf,100)

        #size = draw.textsize(text, font=font)
        #w,h = size
        #if width==None:
            #width = int(w * (float(height)/h))
        #img = Image.new("RGBA",size,(0,0,0,0))
        #draw = ImageDraw.Draw(img)
        #draw.text((0,0), text, color, font=font )
        
        ## The below silliness is because bbox does not work well with truetype fonts.
        #w,h = img.size
        #x1 = int(w)
        #y1 = int(h)
        #x2 = 0
        #y2 = 0
        #for y in xrange(h):
            #for x in xrange(w):
                #alpha = img.getpixel((x,y))[3]
                #if alpha > 0:
                    #x1 = min(x1,x)
                    #x2 = max(x2,x)
                    #y1 = min(y1,y)
                    #y2 = max(y1,y)
        #x2 = min(w,x2+1)
        #y2 = min(h,y2+1)
        #img = img.crop((x1,y1,x2,y2))
        #self.add(HairyPixels(width=width, height=height, image=img))

    def add(self,obj):
        objname = obj.__class__.__name__
        if objname == "HairyPixels":
            self._BUFFER.append(obj)
        elif objname == "HairyBuffer":
            for pixels in obj:
                self._BUFFER.append(pixels)
        else:
            print "Don't know object type" + objname    
        return self
    
    def move(self,x,y,step=None,delay=None):
        if step != None:
            self.target_x = x
            self.target_y = y
            self.target_step = abs(step)
            self.target_delay = delay
        else:
            self.x = x
            self.y = y
        self.path = []
        
    def path(self,x=None,y=None,step=None,delay=None,path=None):
        if path:
            self.target_path += path
        else:
            self.target_path.append((x,y,step,delay))
        
    def move_step(self,time_since_last_update):
        if self.target_delay and self.target_delay > 0:
            self.target_delay -= time_since_last_update
            return None
        
        if self.target_x!=None and self.target_step!=None:
            if abs(self.target_x-self.x) <= self.target_step:
                self.x = self.target_x
                self.target_x = None
            elif self.target_x > self.x:
                self.x += self.target_step
            else:
                self.x -= self.target_step
        if self.target_y!=None and self.target_step!=None:
            if abs(self.target_y-self.y) <= self.target_step:
                self.y = self.target_y
                self.target_y = None
            elif self.target_y > self.y:
                self.y += self.target_step
            else:
                self.y -= self.target_step
#        print self.y, self.target_y, self.target_step
        if len(self.target_path) > 0:
            if (self.target_x == None and self.target_y == None) or (self.target_x == self.x and self.target_y == self.y):
                self.target_x, self.target_y, self.target_step, self.target_delay = self.target_path.pop(0)

    def size(self):
        w = 0
        h = 0
        for frame in self._BUFFER:
            w = max(frame.width,w)
            h = max(frame.height,h)
        return (w,h)
    
    def update(self,width,height):
        try:
            time_since_last_update = time.time() - self.last_update_time
        except:
            time_since_last_update = 0
        self.last_update_time = time.time()
        
        if not self.active:
            return None
        
        if self.start_time != None and self.start_time > 0:
            self.start_time -= time_since_last_update
            return None
        if self.end_time != None:
            if self.end_time > 0:
                self.end_time -= time_since_last_update
            else:
                self.active = False
                self.end_time = None
        
        self.move_step(time_since_last_update)

        if not self.visible:
            return None
        
        if self.FPS > 0 and (self.buffer_step < 0  or (1.0/self.FPS) <= (time.time()-self.last_frame_time)):
            self.buffer_step += 1
            self.last_frame_time = time.time()
            
        if len(self._BUFFER) <= self.buffer_step and self.repeat:
            self.buffer_step = 0

        try:
            return self._BUFFER[self.buffer_step]
        except:
            return False
                            

#############################################################################        
                            
class Hair:
    FPS = 10
    _LAYERS = []
    _SCREEN = None
    client = None
    width = 0
    height = 0
    last_time = time.time()
    
    def __init__(self,width=95,height=16,host="192.168.7.2:7890"): 
        if HAIR_SIM == True:
            host = "localhost:22000"
        self.width = width
        self.height = height
        self.client = opc.Client(host)
        #self._SCREEN = HairyPixels(width,height)
 
    def __len__(self):
        return len(self._LAYERS)
    
    def __getitem__(self,key):
        if type(key).__name__ == 'tuple':
            x,y = key
            return self._SCREEN[x,y]
        else:
            return self._LAYERS[key]
    
    def add(self,obj,align=None):
        objname = obj.__class__.__name__
        if objname == "HairyPixels":
            hb = HairyBuffer()
            hb.add(obj)
        elif objname == "HairyBuffer":
            hb = obj
        else:
            return False
        self._LAYERS.append(hb)

        if align != None:
            w,h = hb.size()
            if align == "CENTER":
                hb.x = int( (self.width - w) / 2 )
                hb.y = int( (self.height - h) / 2 )
        return hb

    def update(self):
        self._SCREEN = HairyPixels(width=self.width, height=self.height, default_pixel=(0,0,0))
        for layer in self._LAYERS:
            pixels = layer.update(width=self.width,height=self.height)
            if pixels != False:
                self._SCREEN.overlay(pixels,x=layer.x,y=layer.y)
        self.client.put_pixels(self._SCREEN.get_raw(), channel=0)
        time.sleep(1.0 / self.FPS)

    #######################################################################################################
    #  Below are shortcut functions which create a HairyBuffer with the proper data
    #  and then return it to the user
    #######################################################################################################
    def load_gif(self,filename=None,image=None,width=None,height=None):
        hb = HairyBuffer()
        hb.add_gif(filename=filename,image=image,width=width,height=height)
        return hb
    
    def load_image(self,filename=None,width=None,height=None,image=None):
        hb = HairyBuffer()
        hb.add_image(filename,width,height,image)
        return hb
        
    def load_sprite(self,filename=None,width=None,height=None,x1=None,y1=None,x2=None,y2=None,image=None):
        hb = HairyBuffer()
        hb.add_sprite(filename,width,height,x1,y1,x2,y2,image)
        return hb
    
    def load_text(self,text,width=None,height=None,color=(255,255,255),ttf=None):
        hb = HairyBuffer()
        hb.add_text(text, width, height, color, ttf)
        return hb
