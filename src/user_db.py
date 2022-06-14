"""
Given a list of user defined kits, this module will create the user's inventory (database) 
"""
import pandas as pd
import numpy as np
from typing import Dict, List, DefaultDict
from collections import defaultdict

mock_inputs = ['8884', '8885']

class UserDatabase:
    """_summary_
    """
    def __init__(self, sets=defaultdict(lambda: 0), parts=defaultdict(lambda: 0)):
        """_summary_

        Args:
            sets (_type_, optional): _description_. Defaults to defaultdict(lambda: 0).
            parts (_type_, optional): _description_. Defaults to defaultdict(lambda: 0).
        """
        self.sets = sets
        self.parts = parts
        self.sets_db = pd.DataFrame()
        self.parts_db = pd.DataFrame()
        
    def add_set(self, set_dict: Dict) -> None:
        for lego_set, cnt in set_dict.items():
            self.sets[lego_set] += cnt
        return
    
    def add_parts(self, parts_dict: Dict) -> None:
        for part, cnt in parts_dict.items():
            self.parts[part] += cnt
        return
    
    def remove_set(self, set_list: Dict) -> None:
        for k, v in set_list.items():
            if k not in self.sets or self.sets[k] == 0:
                print(f'{k} is not found in existing user inventory.')
                continue
            elif v > self.sets[k]:
                print(f'Attempting to remove {v} sets of {k} but only found {self.sets[k]} sets.')
            else:
                self.sets[k] -= v
        return
    
    def remove_parts(self, part_list: Dict) -> None:
        for k, v in part_list.items():
            if k not in self.parts or self.parts[k] == 0:
                print(f'{k} is not found in existing user inventory.')
                continue
            elif v > self.parts[k]:
                print(f'Attempting to remove {v} number of {k} but only found {self.parts[k]} parts.')
            else:
                self.parts[k] -= v
        return
    
    def generate_set_db(self):
        self.sets_db = pd.DataFrame(self.sets)
        return
    
    def generate_parts_list(self):
        self.parts_db = pd.DataFrame(self.parts)
        return
    