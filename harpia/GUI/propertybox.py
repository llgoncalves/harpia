# -*- coding: utf-8 -*-
"""
This module contains the PropertyBox class.
"""
import gi
gi.require_version('Gtk', '3.0')
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import harpia.GUI.components
from gi.repository import Gtk
from gi.repository import Gdk
from harpia.GUI.fieldtypes import *


class PropertyBox(Gtk.VBox):
    """
    This class contains methods related the PropertyBox class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        self.main_window = main_window
        self.block = None
        self.properties = {}
        Gtk.VBox.__init__(self)
        self.set_homogeneous(False)
        self.set_property("border-width", 0)
        white = Gdk.RGBA(1, 1, 1, 1)
        self.override_background_color(Gtk.StateType.NORMAL, white)
        self.show_all()

# ----------------------------------------------------------------------
    def set_block(self, block):
        """
        This method set properties the block.

            Parameters:
                * **block** (:class:`PropertyBox<harpia.GUI.propertybox>`)
            Returns:
                None
        """
        self.block = block
        # First, remove all components
        for widget in self.get_children():
            self.remove(widget)

        # Search block properties to create GUI
        for prop in self.block.get_properties():
            field = self._generate_field(prop.get("name"), prop)
            self.properties[prop.get("name")] = ""
            if prop["type"] == HARPIA_OPEN_FILE or \
                    prop["type"] == HARPIA_SAVE_FILE:
                field.set_parent_window(self.main_window)
            self.pack_start(field, False, False, 0)

# ----------------------------------------------------------------------
    def notify(self, widget=None, data=None):
        """
        This method notify modifications in propertybox
        """
        # It is time to look for values
        self.__recursive_search(self)
        # we have a returnable dictionary, call the callback method
        self.block.set_properties(self.properties)

# ----------------------------------------------------------------------
    def __recursive_search(self, container):
        for widget in container.get_children():
            # If widget is a container, search inside it
            if isinstance(widget, Gtk.Container):
                self.__recursive_search(widget)
            # Once a component is found, search for it on the component list
            if widget.get_name() in self.properties:
                self.properties[widget.get_name()] = widget.get_value()

# ----------------------------------------------------------------------
    def _generate_field(self, component_key, component_attributes):
        type_ = component_attributes["type"]
        field = component_list[type_](component_attributes, self.notify)
        return field

# ----------------------------------------------------------------------
