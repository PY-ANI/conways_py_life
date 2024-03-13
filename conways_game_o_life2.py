#!../bin/python3
import os
import pygame
from collections import defaultdict
from dataclasses import dataclass

@dataclass(init=True,unsafe_hash=True)
class Cell:
    x:int
    y:int
    w:int
    h:int

    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = (x,y,w,h)
        self.gen=0
    
    def __add__(self, oprand:tuple[int,int]):
        temp = Cell(self.x+oprand[0], self.y+oprand[1], self.w, self.h)
        temp.gen=self.gen+1
        return temp

class env():
    pygame.init()
    def __init__(self, width, height):
        self.win_size = pygame.Rect(0,0,width,height)
        self.win = pygame.display.set_mode(self.win_size.bottomright)
        self.left_sec_rect = pygame.Rect(0,0,width-100,height)
        self.right_sec_rect = pygame.Rect(width-200,0,200,height)
        self.tick = pygame.time.Clock().tick
        pygame.display.set_caption(title=__file__.split('\\')[-1],icontitle=__file__.split('\\')[-1])
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        self.fps = 60
        self.block_size = 10
        self.cell_size = 6
        self.cell_offset = 2
        self.curr_epoch = pygame.time.get_ticks()
        self.evo_delay = 100 # in mili second
        
        self.live_cells = set()
        self.adjacent_cell = defaultdict(int)
        self.neighbours = [(x,y) for y in range(-self.block_size,self.block_size*2,self.block_size) for x in range(-self.block_size,self.block_size*2,self.block_size) if (x,y) != (0,0)]
        self.mouse_hold = False
        self.any_update = True
        self.isrunning = False

    def reset(self):
        self.live_cells.clear()
        self.adjacent_cell.clear()
        self.update()

    def is_extinct(self):
        if self.live_cells.__len__() == 0:
            self.isrunning=False
            return True

    def evolve_forward(self):
        if self.is_extinct(): return

        self.adjacent_cell.clear()
        for cell in self.live_cells:
            for ncell in self.neighbours:
                temp = cell+ncell
                if self.left_sec_rect.contains(temp.rect):
                    self.adjacent_cell[temp] += 1

        live_cells = self.live_cells & {cell for cell, n_count in self.adjacent_cell.items() if n_count in (2,3)}

        born_cells = {cell for cell, n_count in self.adjacent_cell.items() if n_count == 3} - self.live_cells

        temp = live_cells|born_cells

        cleanup = self.live_cells - temp
        
        self.live_cells = temp

        for c in cleanup: self.win.fill((0,0,0),c.rect)
        self.draw_live_cells()
        pygame.display.flip()

    def update(self):
        self.win.fill((0,0,0),self.left_sec_rect)
        self.win.fill((200,200,200),self.right_sec_rect)
        self.draw_grid()
        pygame.display.flip()

    def normalize(self, x):
        return x-x%self.block_size+self.cell_offset

    def set_value(self, x, y):
        temp = Cell(x,y,self.cell_size,self.cell_size)
        self.live_cells.add(temp)
        pygame.draw.rect(self.win,(200,0,0),temp)
        pygame.display.update()
    
    def del_value(self, x, y):
        temp = Cell(x,y,self.cell_size,self.cell_size)
        self.live_cells.discard(temp)
        pygame.draw.rect(self.win,(0,0,0),temp)
        pygame.display.update(temp.rect)

    def key_binding(self):
        if click_down:=pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.left_sec_rect.collidepoint(click_down[0].pos):
                self.mouse_hold = click_down[0].button
                if self.mouse_hold == 1:
                    self.set_value(*map(self.normalize, click_down[0].pos))
                elif self.mouse_hold == 3:
                    self.del_value(*map(self.normalize, click_down[0].pos))
        elif click_up:=pygame.event.get(pygame.MOUSEBUTTONUP):
            self.mouse_hold = 0
        elif pygame.event.get(pygame.MOUSEMOTION) and self.mouse_hold:
            if self.mouse_hold == 1:
                self.set_value(*map(self.normalize, pygame.mouse.get_pos()))
            elif self.mouse_hold == 3:
                self.del_value(*map(self.normalize, pygame.mouse.get_pos()))
        
        if key:=pygame.event.get(pygame.KEYDOWN):
            if key[0].key == 32:
                if self.isrunning: self.isrunning=False
                else: self.isrunning=True
            if key[0].key == 8: self.reset()

    def draw_live_cells(self):
        for c in self.live_cells:
            pygame.draw.rect(self.win, (200,c.gen%256,(c.gen//6)%256), c)

    def draw_grid(self):
        for y in range(self.block_size,self.win_size.h,self.block_size):
            for x in range(self.block_size,self.win_size.w,self.block_size):
                pygame.draw.line(self.win, (0,0,100), (x,0), (x,self.win_size.h), 1)
            pygame.draw.line(self.win, (0,0,100), (0,y), (self.win_size.w,y), 1)

    def run(self):
        self.reset()
        while not pygame.event.get(pygame.QUIT):

            self.tick(self.fps)

            self.key_binding()

            if self.isrunning:
                if pygame.time.get_ticks()-self.curr_epoch >= self.evo_delay:
                    self.evolve_forward()
                    self.curr_epoch = pygame.time.get_ticks()
                    

        
        pygame.quit()


if __name__ == "__main__":
    env = env(1000,600)
    env.run()
    os.system("cls")