#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 19.08.2015

@author: DBernhardt
'''
import pygame
import utils

class Hero():
    def __init__(self,canvas):
        # Allgemein
        self.screen = canvas
        # Itemauswahl
        self.imageInfo = {"Body":{"id":0,"name":"BODY_male.png"},
                          "Feet":{"id":0,"name":"FEET_plate_armor_shoes.png"},
                          "Hair":{"id":0,"name":"HEAD_hair_blonde.png"},
                          "Hat":{"id":1,"name":"HEAD_robe_hood.png"},
                          "Legs":{"id":0,"name":"LEGS_pants_greenish.png"},
                          "Torso":{"id":0,"name":"TORSO_leather_armor_shirt_white.png"},
                          "Weapon":{"id":0,"name":"WEAPON_dagger.png"}}
        
        # Animation
        self.animX = 0
        self.animY = 0
        self.anim = 0
        self.anim_list = {0:{"name":"walkcycle","len":9,"order":["Body","Legs","Feet","Torso","Hair","Hat"]},
                          1:{"name":"spellcast","len":7,"order":["Body","Legs","Feet","Torso","Hair","Hat"]},
                          2:{"name":"slash","len":6,"order":["Body","Legs","Feet","Torso","Hair","Hat","Weapon"]}}
        self.anim_run = False
        self.seq = 0
        self.seqmax = 4
        
        # Images
        self.image = {"Legs":None,"Torso":None,"Body":None,"Feet":None,"Weapon":None,"Hair":None,"Hat":None}
        self.whole = {"walkcycle":{"Body":None,"Legs":None,"Torso":None,"Feet":None,"Hair":None,"Hat":None},
                      "spellcast":{"Body":None,"Legs":None,"Torso":None,"Feet":None,"Hair":None,"Hat":None},
                      "slash":{"Body":None,"Legs":None,"Torso":None,"Feet":None,"Hair":None,"Hat":None,"Weapon":None}}
        self.rect = pygame.rect.Rect(0,0,64,64)
    
    def loadImageV2(self):
        for animation in self.whole:
            for part in self.whole[animation]:
                self.whole[animation][part] = utils.simple_load_image(animation+"/"+self.imageInfo[part]["name"], (255,0,255))
                try:
                    self.image[part] = self.whole[animation][part].subsurface((self.animX*64,self.animY*64,64,64))
                except:
                    pass
        self.rect = pygame.rect.Rect(128,100,64,64)
    
    def refreshImage(self, part, anim):
        if part in self.whole[self.anim_list[self.anim]["name"]]:
            self.image[part] = self.whole[self.anim_list[anim]["name"]][part].subsurface((self.animX*64,self.animY*64,64,64))
        else:
            self.image[part] = None
        self.rect = pygame.rect.Rect(128,100,64,64)
    
    def DrawHero(self):
        for part in self.anim_list[self.anim]["order"]:
            if self.image[part] is not None:
                self.screen.blit(self.image[part],self.rect)
    
    def Update(self):
        if self.anim_run:
            if self.seq >= self.seqmax:
                self.seq = 0
                self.animX += 1
                if self.animX >= self.anim_list[self.anim]["len"]:
                    self.animX = 0;
                    self.animY += 1
                    if self.animY >= 4:
                        self.animY = 0
                        self.anim += 1
                        if self.anim >= len(self.anim_list):
                            self.anim = 0
                for item in self.imageInfo:
                    if self.image[item] is not None and str(item) in self.whole[self.anim_list[self.anim]["name"]]:
                        self.refreshImage(item, self.anim)
            self.seq += 1
