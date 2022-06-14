"""_summary_
"""
from src.user_db import UserDatabase
import pytest

class TestUserDatabase:
    @pytest.fixture
    def sample_user(self):
        sample_user = UserDatabase()
        return sample_user
    
    def test_add_set(self, sample_user):
        assert not bool(sample_user.sets)
        sample_user.add_set({'8884': 1, '8885': 2})
        assert sample_user.sets == {'8884': 1, '8885': 2}
        sample_user.add_set({'8884': 2})
        assert sample_user.sets == {'8884': 3, '8885': 2}
        sample_user.add_set({'8886': 1})
        assert sample_user.sets == {'8884': 3, '8885': 2, '8886': 1}
    
    def test_add_parts(self, sample_user):
        assert not bool(sample_user.parts)
        sample_user.add_parts({'11111': 1, '22222': 1})
        assert sample_user.parts != ({'11111': 1, '22222': 2})
        assert sample_user.parts == ({'11111': 1, '22222': 1})
        sample_user.add_parts({'11111': 2})
        assert sample_user.parts == ({'11111': 3, '22222': 1})    
        
    def test_remove_set(self, sample_user, capfd):
        assert bool(sample_user.sets)
        sample_user.remove_set({'8889': 1})
        out, _ = capfd.readouterr()
        assert out == "8889 is not found in existing user inventory.\n"
        sample_user.remove_set({'8884': 4})
        out, _ = capfd.readouterr()
        assert out == 'Attempting to remove 4 sets of 8884 but only found 3 sets.\n'
        sample_user.remove_set({'8884': 2})
        assert sample_user.sets == ({'8884': 1, '8885': 2, '8886': 1})
        sample_user.remove_set({'8884': 1})
        assert sample_user.sets['8884'] == 0
        sample_user.remove_set({'8884': 1})
        out, _ = capfd.readouterr()
        assert out == "8884 is not found in existing user inventory.\n"
    
    def test_remove_parts(self, sample_user, capfd):
        assert bool(sample_user.parts)
        sample_user.remove_parts({'33333': 1})
        out, _ = capfd.readouterr()
        assert out == "33333 is not found in existing user inventory.\n"
        sample_user.remove_parts({'11111': 100})
        out, _ = capfd.readouterr()
        assert out == 'Attempting to remove 100 number of 11111 but only found 3 parts.\n'
        sample_user.remove_parts({'11111': 3})
        assert sample_user.parts == ({'11111': 0, '22222': 1})
        