
from .label import Label


FREE_TEXT = 'free_text'

class FreeText(Label):
    '''Free text is basically just a Label
    
    Suppose in future can check min, max length, etc

    But for now, main things are:
        - dtype is object
        - either has or does not have nans
    '''
    pass
