#!../bin/python3

import json
import os
import pygame
from collections import defaultdict
from dataclasses import dataclass

class label():
    def __init__(self,win:pygame.Surface,x:int,y:int,text:str="",size:int=10):
        self.win = win
        self.surf = pygame.font.Font("fonts/KodeMono-SemiBold.ttf",size).render(text,True,(20,20,20))
        self.rect = self.surf.get_rect(topleft=(x,y))

    def draw(self):
        self.win.blit(self.surf, self.rect)

class btn():
    def __init__(self,win:pygame.Surface,x:int,y:int,width:None|int=None,height:None|int=None,text:str="",size:int=10):
        self.win = win
        self.surf = pygame.font.Font("fonts/KodeMono-SemiBold.ttf",size).render(text,True,(20,20,20))
        self.rect = self.surf.get_rect(topleft=(x,y))

    def draw(self):
        self.win.blit(self.surf, self.rect)
        pygame.draw.rect(self.win,(0,0,0),self.rect,1,2)

class live_label():
    def __init__(self,win:pygame.Surface,x:int,y:int,width:int,height:int,size:int=10):
        self.win = win
        self.font_kernel = pygame.font.Font("fonts/KodeMono-SemiBold.ttf",size)
        self.rect = pygame.Rect(x,y,width,height)

    def render(self,text:str):
        self.win.fill((200,200,200), self.rect)
        tsurf = self.font_kernel.render(text,True,(20,20,20))
        trect = tsurf.get_rect(center=self.rect.center)
        self.win.blit(tsurf, trect)
        pygame.display.update(self.rect)

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
        self.gen = 0
        self.rect = (x,y,w,h)

    def __add__(self, oprand:tuple[int,int]):
        temp = Cell(self.x+oprand[0], self.y+oprand[1], self.w,self.h)
        temp.gen=self.gen+1
        return temp


class env():
    pygame.init()
    def __init__(self, width, height):
        # env config
        self.win_size = pygame.Rect(0,0,width,height)
        self.left_sec_rect = pygame.Rect(0,0,width-150,height)
        self.right_sec_rect = pygame.Rect(width-150,0,150,height)
        self.fps = 60
        self.block_size = 5
        self.cell_size = 5
        # self.cell_offset = 2
        self.evo_delay = 100 # in mili second        
        self.mouse_hold = False
        self.any_update = True
        self.isrunning = False
        self.generation = 0
        # env vars
        self.win = pygame.display.set_mode(self.win_size.bottomright)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title=__file__.split('\\')[-1],icontitle=__file__.split('\\')[-1])
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        self.curr_epoch = pygame.time.get_ticks()
        self.live_cells = set()
        self.adjacent_cell = defaultdict(int)
        self.neighbours = [(x,y) for y in range(-1,2,1) for x in range(-1,2,1) if (x,y) != (0,0)]
        # right section
        self.labels = [
            label(self.win,self.right_sec_rect.x,4,text="-File--------",size=18),
            label(self.win,self.right_sec_rect.x,100,text="-Env-Control-",size=18),
            label(self.win,self.right_sec_rect.x,300,text="-Env-Status--",size=18),
            label(self.win,self.right_sec_rect.x+10,130,text=">Evo Delay",size=14),
            label(self.win,self.right_sec_rect.x+10,330,text=">EVO-Generation",size=14),
            label(self.win,self.right_sec_rect.x+10,370,text=">Live-Cell-Count",size=14),
            ]
        self.buttons = [
            btn(self.win,self.right_sec_rect.x+10,40,text=" Load  ",size=16),
            btn(self.win,self.right_sec_rect.x+10,70,text=" Export  ",size=16),
            btn(self.win,self.right_sec_rect.x+10,150,text=" + ",size=16),
            btn(self.win,self.right_sec_rect.right-40,150,text=" - ",size=16),
            ]
        self.evo_delay_label = live_label(self.win,self.right_sec_rect.centerx-30,150,60,20,14)
        self.gen_count_label = live_label(self.win,self.right_sec_rect.centerx-30,350,60,20,14)
        self.live_cell_label = live_label(self.win,self.right_sec_rect.centerx-30,390,60,20,14)
        self.action_list = [
            self.load_pattern,
            self.save_pattern,
            self.increase_delay,
            self.decrease_delay,
        ]

    def load_pattern(self):
        pass

    def save_pattern(self):
        pass

    def increase_delay(self):
        self.evo_delay += 50 if self.evo_delay < 1000 else 0
        self.evo_delay_label.render(str(self.evo_delay))

    def decrease_delay(self):
        self.evo_delay -= 50 if self.evo_delay > 0 else 0
        self.evo_delay_label.render(str(self.evo_delay))

    def reset(self):
        self.generation = 0
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
                temp = cell+tuple(map(lambda x:x*self.block_size, ncell))
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
        self.generation += 1

    def update(self):
        self.win.fill((0,0,0),self.left_sec_rect)
        self.draw_grid()
        self.draw_menu()
        pygame.display.flip()

    def normalize(self, x):
        return x-x%self.block_size # +self.cell_offset

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
            else:
                for i, func in enumerate(self.action_list):
                    rect = self.buttons[i].rect
                    if rect.collidepoint(click_down[0].pos):
                        func()
                        break
        elif click_up:=pygame.event.get(pygame.MOUSEBUTTONUP):
            self.mouse_hold = 0
        elif pygame.event.get(pygame.MOUSEMOTION) and self.mouse_hold:
            m_pos = pygame.mouse.get_pos()
            if self.left_sec_rect.collidepoint(m_pos):
                if self.mouse_hold == 1:
                    self.set_value(*map(self.normalize, m_pos))
                elif self.mouse_hold == 3:
                    self.del_value(*map(self.normalize, m_pos))
        
        if key:=pygame.event.get(pygame.KEYDOWN):
            if key[0].key == 32:
                if self.isrunning: self.isrunning=False
                else: self.isrunning=True
            if key[0].key == 8: self.reset()

    def draw_menu(self):
        self.win.fill((200,200,200),self.right_sec_rect)
        for label in self.labels: label.draw()
        for button in self.buttons: button.draw()
        self.evo_delay_label.render(str(self.evo_delay))
        self.gen_count_label.render(str(self.generation))
        self.live_cell_label.render(str(self.live_cells.__len__()))
    
    def draw_live_cells(self):
        for c in self.live_cells:
            pygame.draw.rect(self.win, (200,c.gen%256,(c.gen//6)%256), c)

    def draw_grid(self):
        for y in range(self.block_size,self.left_sec_rect.h,self.block_size):
            for x in range(self.block_size,self.left_sec_rect.w,self.block_size):
                pygame.draw.line(self.win, (0,0,100), (x,0), (x,self.left_sec_rect.h), 1)
            pygame.draw.line(self.win, (0,0,100), (0,y), (self.left_sec_rect.w,y), 1)

    def run(self):
        self.reset()
        while not pygame.event.get(pygame.QUIT):

            # self.clock.tick(self.fps)

            self.key_binding()

            if self.evo_delay == 0 or pygame.time.get_ticks()-self.curr_epoch >= self.evo_delay:
                if self.isrunning:
                    self.evolve_forward()
                    self.gen_count_label.render(str(self.generation))
                    self.live_cell_label.render(str(self.live_cells.__len__()))
                    self.curr_epoch = pygame.time.get_ticks()
        
        pygame.quit()


if __name__ == "__main__":
    env = env(1000,600)
    env.run()
    os.system("clear")