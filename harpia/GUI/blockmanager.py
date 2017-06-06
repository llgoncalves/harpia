#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the BlockManager class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicomponents.stringfield import StringField
from mosaicomponents.combofield import ComboField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.codefield import CodeField
from mosaicomponents.openfilefield import OpenFileField
from harpia.GUI.blocknotebook import BlockNotebook
from harpia.GUI.fieldtypes import *
from harpia.GUI.blockeditor import BlockEditor
from harpia.GUI.dialog import Dialog
from harpia.model.plugin import Plugin
from harpia.system import System as System
import gettext

_ = gettext.gettext


class BlockManager(Gtk.Dialog):
    """
    This class contains methods related the BlockManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, _("Block Manager"), main_window, 0, ())

        self.main_window = main_window
        self.main_control = self
        self.set_default_size(400, 300)
        box = self.get_content_area()
        vbox = Gtk.VBox()
        box.pack_start(vbox, True, True, 0)

        # Block List
        self.block_notebook = BlockNotebook(self)

        # Button bar
        button_bar = Gtk.HBox()
        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        button.connect("clicked", self.__new, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EDIT)
        button.connect("clicked", self.__edit, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_DELETE)
        button.connect("clicked", self.__delete, None)
        button_bar.pack_start(button, False, False, 0)

        vbox.pack_start(self.block_notebook, True, True, 0)
        vbox.pack_start(button_bar, False, False, 0)

        self.show_all()
        self.show()

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        BlockEditor(self, Plugin())

    # ----------------------------------------------------------------------
    def __edit(self, widget=None, data=None):
        block = self.block_notebook.get_selected_block()
        if block is None:
            return
        BlockEditor(self, block)

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        block = self.block_notebook.get_selected_block()
        if block is None:
            return
        dialog = Dialog().confirm_dialog(_("Are you sure?"), self)
        result = dialog.run()
        dialog.destroy()
        if result == Gtk.ResponseType.OK:
            self.main_window.main_control.delete_block(block)
            self.update()

    # ----------------------------------------------------------------------
    def set_block(self, block):
        """
        This method is called when a block is selected. Nothing to do here.
            Parameters:
                block
            Returns:
                None.
        """
        pass

    # ----------------------------------------------------------------------
    def add_block(self, block):
        """
        This method is called when a block is double clicked.

            Parameters:
                * **block** (:class:`<>`)
        """
        BlockEditor(self, self.block_notebook.get_selected_block())

    # ----------------------------------------------------------------------
    def add_block(self, block):
        self.main_window.main_control.add_block(block)

    # ----------------------------------------------------------------------
    def update(self):
        self.block_notebook.update()
# ----------------------------------------------------------------------
