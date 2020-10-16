
from . import DataUnit


LABEL = 'label'

class Label(DataUnit):
    '''When to use label:
        When you have strings where it doesnt matter what those values are.
        In this case, the primary thing to look at is `hasna`
        Most of the time, if an abstract highly varying string is expected,
        you'll not want there to be any nas
    '''
    def profile(self, data):
        profile = {}
        return profile
    
    def verify(self, data, profile):
        '''cop out class, nothing to verify'''
        error_reports = []
        return error_reports
