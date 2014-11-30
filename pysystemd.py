#!/usr/bin/env python
from gi.repository import Gio, GLib

'''
DBUS API of systemd http://www.freedesktop.org/wiki/Software/systemd/dbus/
JOBMODE's http://cgit.freedesktop.org/systemd/systemd/tree/src/core/job.h#n84
http://cgit.freedesktop.org/systemd/systemd/tree/src/core/dbus-manager.c#n1853
GLIB docs http://valadoc.org/#!api=gio-2.0/GLib.DBusProxy

public Variant call_sync (string method_name, Variant? parameters, DBusCallFlags flags, int timeout_msec, Cancellable? cancellable = null) throws Error

'''

class Unit:
    def __init__(self, unit, proxy):
        self.data = unit
        self.proxy = proxy
        (self.name, self.descrip, self.load, self.active, self.sub, _, self.interface, _, _, _) = self.data

    def start(self): # TODO: add JOBMODE flag
        self.proxy.call_sync('StartUnit', GLib.Variant('(ss)', (self.name, 'replace',)), Gio.DBusCallFlags.NONE, -1, None)

    def stop(self): 
        self.proxy.call_sync('StopUnit', GLib.Variant('(ss)', (self.name, 'replace',)), Gio.DBusCallFlags.NONE, -1, None)

    def __repr__(self):
        return '%s(%s)' % (self.name, self.descrip)




class SystemdManager:
    def __init__(self):
        self.bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        self.proxy = Gio.DBusProxy.new_sync(self.bus, Gio.DBusProxyFlags.NONE, None, 'org.freedesktop.systemd1', '/org/freedesktop/systemd1', 'org.freedesktop.systemd1.Manager', None)

    def listunits(self):
        unitsvariant = self.proxy.call_sync('ListUnits', None, Gio.DBusCallFlags.NONE, -1, None)
        (units,) = unitsvariant.unpack() # Returns a list with tuples
        return [Unit(unit, self.proxy) for unit in units]

    def listunitfiles(self):
        unitsvariant = self.proxy.call_sync('ListUnitFiles', None, Gio.DBusCallFlags.NONE, -1, None)
        (units,) = unitsvariant.unpack() # Returns a list with tuples
        return units
