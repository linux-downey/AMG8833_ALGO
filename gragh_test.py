import pygame
import threading
import multiprocessing

from colour import Color

GR_HEIGHT = 400
GR_WIDTH = GR_HEIGHT * 3 


all_pixels_num =64

sensor_data = [29.8888]*all_pixels_num
bk_grd_data = [27.888]*all_pixels_num

pixels_row = 8
pixels_colum = 8
height = 480
width  = 480

pixels_size_height = height /pixels_colum
pixels_size_width = width /pixels_row

num_color = (0,0,0)

resolution = (height,width )
num_size = height / pixels_row /2

max_temp = 31
min_temp = 26

color_resolution = 100

blue = Color("blue")
#list() turn the tuple to list.
colors = list(blue.range_to(Color("red"), color_resolution))
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
#print colors

def select_color(val):
    if (val< min_temp):
        return 0
    return int((float(val)-min_temp)/(max_temp-min_temp) *color_resolution -1)
    

def conver_val_to_str(value):
    val_str=str(value)
    val_str=val_str[0:4]
    return val_str

def raw():
    while(1):
        pygame.init()
        gragh=pygame.display.set_mode( resolution)
        gragh.fill((0,0,0))
        font = pygame.font.Font(None, num_size)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("raw data!")
        for i in range(pixels_row):
            for j in range(pixels_colum):
                pygame.draw.rect(gragh,colors[select_color(sensor_data[pixels_row*i+j])],(i*pixels_size_width,j*pixels_size_height,pixels_size_width,pixels_size_height))
                num=font.render(conver_val_to_str(sensor_data[pixels_row*i+j]),0,num_color)
                gragh.blit(num,(i*pixels_size_width,j*pixels_size_height))
        
        pygame.display.update()
        
        while 1:
            pass

def back():
    while 1:
        while(1):
        pygame.init()
        gragh=pygame.display.set_mode( resolution)
        gragh.fill((0,0,0))
        font = pygame.font.Font(None, num_size)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("raw data!")
        for i in range(pixels_row):
            for j in range(pixels_colum):
                pygame.draw.rect(gragh,colors[select_color(bk_grd_data[pixels_row*i+j])],(i*pixels_size_width,j*pixels_size_height,pixels_size_width,pixels_size_height))
                num=font.render(conver_val_to_str(bk_grd_data[pixels_row*i+j]),0,num_color)
                gragh.blit(num,(i*pixels_size_width,j*pixels_size_height))
        
        pygame.display.update()
        
        while 1:
            pass

def ther():
    while 1:
        while(1):
        pygame.init()
        gragh=pygame.display.set_mode( resolution)
        gragh.fill((0,0,0))
        font = pygame.font.Font(None, num_size)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("raw data!")
        for i in range(pixels_row):
            for j in range(pixels_colum):
                pygame.draw.rect(gragh,colors[select_color(sensor_data[pixels_row*i+j])],(i*pixels_size_width,j*pixels_size_height,pixels_size_width,pixels_size_height))
                num=font.render(conver_val_to_str(sensor_data[pixels_row*i+j]),0,num_color)
                gragh.blit(num,(i*pixels_size_width,j*pixels_size_height))
        
        pygame.display.update()
        
        while 1:
            pass

P1=multiprocessing.Process(target = raw)
P2=multiprocessing.Process(target = back)
P3=multiprocessing.Process(target = ther)
P1.start()
P2.start()
P3.start()


'''
pygame.init()
raw_t = threading.Thread( target = raw)
bk_grd_t = threading.Thread(target = back)
#ther_t = threading.Thread(target = ther)

raw_t.start()

bk_grd_t.start()
#ther_t.start()
raw_t.join()
'''
