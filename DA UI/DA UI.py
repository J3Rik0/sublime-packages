"""
DA UI

Copyright (c) 2017, Ihor Oleksandrov.
Unauthorized copying of this file, via any medium is strictly
prohibited.
"""


import sublime

from .modules import package
from .modules import messages

from .modules.settings import loader
from .modules.utils import cleaner
from .modules.utils import reloader

from .modules.commands import *
from .modules.listeners import *


def ensure_reload():
    """
    Ensure all modules reload to initialize plugin successfully.
    """
    active_view = sublime.active_window().active_view()
    active_view.set_status("daui_status", messages.START_UPGRADE)

    def erase_status():
        active_view.erase_status("daui_status")

    def reload():
        reloader.reload_plugin()
        active_view.set_status("daui_status", messages.FINISH_UPGRADE)
        sublime.set_timeout(erase_status, 3000)

    sublime.set_timeout(reload, 7000)


def plugin_loaded():
    """
    DA UI loaded.
    """
    cleaner.cleanup()

    was_upgraded = False

    try:
        from package_control import events
    except ImportError:
        pass
    else:
        was_upgraded = events.post_upgrade(package.NAME)
    finally:
        if was_upgraded:
            ensure_reload()
        else:
            loader.load()


def plugin_unloaded():
    """
    DA UI unloaded.
    """
    loader.unload()
