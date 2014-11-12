# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 13:58:03 2014

@author: jniemeye
"""

class Thing():
    def __init__(self, thing1, thing2):
        self.thing1 = thing1
        self.thing2 = thing2
        
    def tada(self, boop):
        print(self.thing1 + boop + self.thing2)
        
this_thing = Thing('this', 'that')
that_thing = Thing('that', 'this')
        
this_thing.tada('merp')

object_list = [this_thing, that_thing]