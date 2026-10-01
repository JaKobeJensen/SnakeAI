import os
import sys


def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base, relative_path)
