"""
Given a list of user defined kits, this module will create the user's inventory (database) 
"""
from typing import Dict
from collections import defaultdict
import pandas as pd

mock_inputs = ['8884', '8885']

class UserDatabase:
    """class
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
        """_summary_

        Args:
            set_dict (Dict): _description_
        """
        for lego_set, cnt in set_dict.items():
            self.sets[lego_set] += cnt
        return
    
    def add_parts(self, parts_dict: Dict) -> None:
        """_summary_

        Args:
            parts_dict (Dict): _description_
        """
        for part, cnt in parts_dict.items():
            self.parts[part] += cnt
        return
    
    def remove_set(self, set_list: Dict) -> None:
        """_summary_

        Args:
            set_list (Dict): _description_
        """
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
        """_summary_

        Args:
            part_list (Dict): _description_
        """
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
        """_summary_
        """
        self.sets_db = pd.DataFrame(self.sets)
        return
    
    def generate_parts_list(self):
        """_summary_
        """
        self.parts_db = pd.DataFrame(self.parts)
        return
    