#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 19.08.2015

@author: Zwiebelkopf
'''

import pygame

import hero
import utils

class starter():
    def __init__(self):
        self.TICKS_PER_SECOND = 30.0
        self.MAX_FRAME_SKIP = 5.0
        self.RESO = 320,240
        
        #some Colors
        self.WHITE = (255,255,255)
        self.BLACK = (  0,  0,  0)
        self.BLUE =  (  0,  0,255)
        self.INVIS = (255,  0,255)
        
        # (Global)Game objects.
        self.game_ticks = 0
        self.clock = None
        self.screen = None
        self.font = pygame.font.Font(None, 26)
        
        
        # Namen der einzelnen Teile
        self.equip = {"Body":{0:"BODY_male.png",1:"BODY_skeleton.png"},
                      "Feet":{0:"FEET_plate_armor_shoes.png",1:"FEET_shoes_brown.png"},
                      "Hair":{0:"HEAD_hair_blonde.png"},
                      "Hat":{0:"HEAD_chain_armor_helmet.png",1:"HEAD_robe_hood.png",2:"HEAD_leather_armor_hat.png"},
                      "Legs":{0:"LEGS_pants_greenish.png",1:"LEGS_plate_armor_pants.png",2:"LEGS_robe_skirt.png"},
                      "Torso":{0:"TORSO_leather_armor_shirt_white.png",1:"TORSO_robe_shirt_brown.png",2:"TORSO_chain_armor_torso.png",3:"TORSO_plate_armor_torso.png"},
                      "Weapon":{0:"WEAPON_dagger.png",1:"WEAPON_whatever.png"}}
        
        self.auswahl_liste = {0:"Body",1:"Legs",2:"Torso",3:"Feet",4:"Weapon",5:"Hair",6:"Hat"}
    
    def update_gameclock(self):
        self.game_ticks += 1
        
        self.char.Update()
        
        if self.game_ticks >= self.clock.ticks_per_second:
            self.set_caption()
            self.game_ticks = 0

    def display_gameclock(self, interpolation):
        
        self.char.DrawHero()
        
        self.screen.blit(self.anim_text, self.anim_text.get_rect(left=70,top=20))
        self.screen.blit(self.auswahl_text, self.auswahl_text.get_rect(left=70,top=40))
        
        pygame.display.update()

    def set_caption(self, value="Hallo Welt!"):
        pygame.display.set_caption(value)
    
    def main(self):
        
        self.screen = pygame.display.set_mode(self.RESO)
        pygame.key.set_repeat(1, 30)
        self.running = True
        self.clock = utils.GameClock(*(self.TICKS_PER_SECOND, 0))
        self.clock.use_wait = False
        
        self.char = hero.Hero(self.screen)
        self.char.loadImageV2()
        
        self.test = pygame.sprite.Sprite()
        self.test.whole = utils.simple_load_image("walkcycle/"+self.equip["Body"][0],self.INVIS)
        self.test.image = self.test.whole.subsurface((0,128,64,64))
        self.test.rect = pygame.rect.Rect(100,100,64,64)
        
        self.auswahl = 0
        self.auswahl_text = self.font.render(self.auswahl_liste[self.auswahl] + ": 0", 1, self.WHITE)
        self.anim_text = self.font.render("Animation: "+str(self.char.anim_run),1,self.WHITE)
        
        while self.running:
            self.screen.fill((0,0,0))
            self.clock.tick()
            if self.clock.update_ready:
                self.update_gameclock()
            if self.clock.frame_ready:
                self.display_gameclock(self.clock.interpolate)
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                
                if e.type == pygame.KEYUP:
                    # Links/Rechts für Spriteauswahl
                    if e.key == pygame.K_RIGHT:
                        self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"] += 1
                        if self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"] >= len(self.equip[self.auswahl_liste[self.auswahl]]):
                            self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"] = 0
                        self.char.imageInfo[self.auswahl_liste[self.auswahl]]["name"] = self.equip[self.auswahl_liste[self.auswahl]][self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"]]
                        
                        self.auswahl_text = self.font.render(self.auswahl_liste[self.auswahl]+": "+str(self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"]), 1, self.WHITE)
                        self.char.loadImageV2()
                    elif e.key == pygame.K_LEFT:
                        self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"] -= 1
                        if self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"] < 0:
                            self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"] = len(self.equip[self.auswahl_liste[self.auswahl]])-1
                        self.char.imageInfo[self.auswahl_liste[self.auswahl]]["name"] = self.equip[self.auswahl_liste[self.auswahl]][self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"]]
                        
                        self.auswahl_text = self.font.render(self.auswahl_liste[self.auswahl]+": "+str(self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"]), 1, self.WHITE)
                        self.char.loadImageV2()
                    # Hoch/Runter für Körperteilasuswahl
                    if e.key == pygame.K_UP:
                        self.auswahl -= 1
                        if self.auswahl < 0:
                            self.auswahl = len(self.auswahl_liste)-1
                        self.auswahl_text = self.font.render(self.auswahl_liste[self.auswahl]+": "+str(self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"]), 1, self.WHITE)
                    elif e.key == pygame.K_DOWN:
                        self.auswahl += 1
                        if self.auswahl >= len(self.auswahl_liste):
                            self.auswahl = 0
                        self.auswahl_text = self.font.render(self.auswahl_liste[self.auswahl]+": "+str(self.char.imageInfo[self.auswahl_liste[self.auswahl]]["id"]), 1, self.WHITE)
                    
                    # Animation starten
                    if e.key == pygame.K_RETURN:
                        self.char.anim_run = not self.char.anim_run
                        self.anim_text = self.font.render("Animation: "+str(self.char.anim_run),1,self.WHITE)
                    
                    if e.key == pygame.K_SPACE:
                        print self.char.anim
                        print self.char.anim_list[self.char.anim]
                        print self.char.whole[self.char.anim_list[self.char.anim]["name"]]
if __name__ == '__main__':
    pygame.init()
    app = starter()
    app.main()
