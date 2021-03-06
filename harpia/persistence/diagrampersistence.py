# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the DiagramPersistence class.
"""
import os
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from harpia.utils.XMLUtils import XMLParser
from harpia.system import System as System


class DiagramPersistence():
    """
    This class contains methods related the DiagramPersistence class.
    """
    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, diagram):

        # load the diagram
        parser = XMLParser(diagram.file_name)

        zoom = parser.getTag("harpia").getTag("zoom").getAttr("value")
        diagram.zoom = float(zoom)
        try:
            language = parser.getTag("harpia").getTag(
                "language").getAttr("value")
            diagram.language = language
        except:
            pass

        # new version load
        blocks = parser.getTag("harpia").getTag(
            "blocks").getChildTags("block")
        for block in blocks:
            block_type = block.getAttr("type")
            if block_type not in System.plugins:
                continue
            block_id = int(block.getAttr("id"))
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")
            properties = block.getChildTags("property")
            props = {}
            for prop in properties:
                try:
                    props[prop.key] = prop.value
                except:
                    pass
            new_block = System.plugins[block_type]
            new_block.set_properties(props)
            new_block.id = block_id
            new_block.x = float(x)
            new_block.y = float(y)
            diagram.add_block(new_block)

        connections = parser.getTag("harpia").getTag(
            "connections").getChildTags("connection")
        for conn in connections:
            try:
                from_block = diagram.blocks[
                    int(conn.getAttr("from_block"))]
                to_block = diagram.blocks[int(conn.getAttr("to_block"))]
            except:
                continue
            from_block_out = int(conn.getAttr("from_out"))
            to_block_in = int(conn.getAttr("to_in"))
            diagram.start_connection(from_block, int(from_block_out) - 1)
            diagram.end_connection(to_block, int(to_block_in) - 1)
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, diagram):
        """
        This method save a file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """

        parser = XMLParser()
        parser.addTag('harpia')
        parser.appendToTag('harpia', 'version', value=System.VERSION)
        parser.appendToTag('harpia', 'zoom', value=diagram.zoom)
        parser.appendToTag('harpia', 'language', value=diagram.language)

        parser.appendToTag('harpia', 'blocks')
        for block_id in diagram.blocks:
            block_type = diagram.blocks[block_id].type
            pos = diagram.blocks[block_id].get_position()
            parser.appendToTag('blocks', 'block', type=block_type, id=block_id)
            parser.appendToLastTag('block', 'position', x=pos[0], y=pos[1])
            props = diagram.blocks[block_id].get_properties()
            for prop in props:
                parser.appendToLastTag('block',
                                       'property',
                                       key=str(prop["name"]),
                                       value=str(prop["value"])
                                       )

        parser.appendToTag('harpia', 'connections')
        for connector in diagram.connectors:
            parser.appendToTag('connections', 'connection',
                               from_block=connector.source.id,
                               from_out=int(connector.source_port) + 1,
                               to_block=connector.sink.id,
                               to_in=int(connector.sink_port) + 1)

        try:
            save_file = open(str(diagram.file_name), "w")
            save_file.write(parser.prettify())
            save_file.close()
        except IOError as e:
            System.log(e.strerror)
            return False, e.strerror

        diagram.set_modified(False)
        return True, "Success"
# ------------------------------------------------------------------------------
