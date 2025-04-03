from ._anvil_designer import FavColorCellTemplate
from anvil import *
import anvil.js

class FavColorCell(FavColorCellTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        # item is the row data we can use for data bindings 
        # we need to close the editor on blur
        tb_node = anvil.js.get_dom_node(self.text_box_1)
        tb_node.addEventListener("blur", self.text_box_1_lost_focus)

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.text_box_1_lost_focus()

    def text_box_1_lost_focus(self, *e, **event_args):
        """This method is called when the TextBox loses focus"""
        self.raise_event("x-close-editor", value=self.text_box_1.text)
