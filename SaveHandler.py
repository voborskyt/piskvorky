# Proto třída
import pygame

class SaveHandler:
    def __init__(self,  SETTING):
        self.SETTING =  SETTING
    def click(self):
        self.SETTING["SAVE"] = True