# Proto třída
import pygame

class StartStopHandler:
    def __init__(self,  SETTING):
        self.SETTING =  SETTING
    def click(self):
        if self.SETTING["RUN"]:
            self.SETTING["RUN"] = False
        else:
            self.SETTING["RUN"] = True