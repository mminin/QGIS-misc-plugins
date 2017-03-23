# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SortLayers
                                 A QGIS plugin
 Sorts layers in Layers Panel alphabetically
                              -------------------
        begin                : 2017-03-23
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Mikhail Minin
        email                : m.minin@jacobs-university.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core    import QgsProject
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui  import QAction,   QIcon,       QMenu
import resources

class SortLayers:
    def __init__(self, iface):
        self.iface     = iface
        self.actions   = []
        self.menuLayer = self.iface.mainWindow().menuBar().findChild(QMenu, 'mLayerMenu')
        self.toolbar   = self.iface.addToolBar(u'SortLayers')
        self.toolbar.setObjectName(u'SortLayers')

    def create_action(self, icon_path, text, callback):
        """Create new action to add to the menu"""
        action = QAction(QIcon(icon_path), text, self.iface.mainWindow())
        action.triggered.connect( callback   )
        action.setEnabled(        True       )
        self.toolbar.addAction(   action     )
        self.menuLayer.addAction( action     )
        self.actions.append(      action     )

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.create_action(
            icon_path = ':/plugins/SortLayers/iconAZ.png',
            text      = u'Sort Layers: A=>Z',
            callback  = self.run)
        self.create_action(
            icon_path = ':/plugins/SortLayers/iconZA.png',
            text      = u'Sort Layers: Z=>A',
            callback  = lambda: self.run(True))

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.menuLayer.removeAction(  action )
            self.iface.removeToolBarIcon( action )
        del self.toolbar

    def run(self, backward=False):
        """Run method that actually sorts layers"""
        root = QgsProject.instance().layerTreeRoot()
        LayerNamesEnumDict=lambda listCh: {listCh[q[0]].layerName()+str(q[0]):q[1]
                                           for q in enumerate(listCh)}
        mLNED     = LayerNamesEnumDict(root.children())
        mLNEDkeys = mLNED.keys()
        mLNEDkeys.sort()
        mLNEDsorted = [mLNED[k].clone() for k in mLNEDkeys]
        if backward: mLNEDsorted=mLNEDsorted[::-1]
        root.insertChildNodes(0,mLNEDsorted)
        for n in mLNED.values(): root.removeChildNode(n)
        
