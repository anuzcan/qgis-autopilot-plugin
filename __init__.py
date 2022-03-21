#-----------------------------------------------------------
# Copyright (C) 2022 Pablo Nuñez
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------
def classFactory(iface):
    
    from .main import Main_Plugin
    return Main_Plugin(iface)

