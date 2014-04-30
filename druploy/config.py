# vim: set syntax=python ts=4 sw=4 expandtab:
import yaml
from druploy.utils import Utils

class Config (object):
    """
    Configuration parsing for druploy.
    """
    @staticmethod
    def load(filename, element):
        config = None
        f = open(filename)
        try:
            config = yaml.safe_load(f)[element]
        except KeyError:
            Utils.error("The '{0}' element was not found in '{1}'.".format(element, filename))
        finally:
            f.close()
        return config
