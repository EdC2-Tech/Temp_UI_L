from ._anvil_designer import MultiSelectDropDownTemplate
from anvil import *
import anvil.server

class MultiSelectDropDown(MultiSelectDropDownTemplate):
  def __init__(self, **properties):
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)

    # If we've been told items can only be selected once...
    if self.unique:
      # .. adding items to the TokenBox removes them from the DropDown ...
      self.token_box.add_callback = lambda token: self.remove_from_dropdown(token.text)
      # .. and removing items from the TokenBox adds them to the DropDown!
      self.token_box.remove_callback = lambda token: self.add_to_dropdown(token.text)

  @property
  def items(self):
    return self.drop_down_1.items

  @items.setter
  def items(self, value):
    if len(value) and value[0] is not self.placeholder:
      self.drop_down_1.items = [self.placeholder] + value
    else:
      self.drop_down_1.items = value
  
  def add_to_dropdown(self, value):
    """Add an item to the DropDown's items list."""
    self.drop_down_1.items = self.drop_down_1.items + [value]

  def remove_from_dropdown(self, text):
    """Remove an item from the DropDown's items list."""
    items = self.drop_down_1.items
    items.remove(text)
    self.drop_down_1.items = items

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.token_box.add(event_args['sender'].selected_value)
    # Go back to having self.placeholder selected, to allow the same value 
    # to be selected multiple times.
    self.drop_down_1.selected_value = self.placeholder
