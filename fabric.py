"""Fabric."""

import os
import copy
from configparser import ConfigParser


def config_path(path):
    """Configuration file path."""
    folder = os.path.dirname(__file__)
    return os.path.join(folder, 'resources', path)


class Fabric:
    """Object fabric."""

    def __init__(self, filename):
        """Constructor."""
        self.storage = dict()
        self._initialize(filename)

    def _initialize(self, filename):
        """Initialize."""
        parser = ConfigParser()
        self.storage = dict()
        parser.read(config_path(filename))
        for section in parser.sections():
            self._process_section(parser[section], section)

    def _process_section(self, data, section):
        """Virtual method."""

    def names(self):
        """Show all objects in storage."""
        return list(self.storage.keys())

    def get_object(self, object_name):
        """Create object."""
        assert object_name in self.storage.keys(), 'Invalid object type'
        return copy.deepcopy(self.storage[object_name])
