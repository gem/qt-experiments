# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Svir
                                 A QGIS plugin
 OpenQuake Social Vulnerability and Integrated Risk
                              -------------------
        begin                : 2013-10-24
        copyright            : (C) 2014 by GEM Foundation
        email                : devops@openquake.org
 ***************************************************************************/

# Copyright (c) 2010-2013, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.
"""
import copy
from PyQt4.QtCore import QThread, pyqtSignal
from process_layer import ProcessLayer
from globals import PROJECT_TEMPLATE
from qgis.core import (QgsVectorLayer, QgsMapLayerRegistry, QgsMessageLog)
from qgis.gui import QgsMessageBar
from utils import (tr, WaitCursorManager)
from import_sv_data import SvDownloadError


class DownloadThread(QThread):
    # This defines a signal called 'rangeChanged' that takes two
    # integer arguments.
    download_done = pyqtSignal(name='download_done')

    def __init__(self, svir, dlg, sv_downloader):
        print "Inside init"
        self.svir = svir
        self.dlg = dlg
        self.sv_downloader = sv_downloader
        QThread.__init__(self)

    def run(self):
        print "Inside thread"
        # TODO: We should fix the workflow in case no geometries are
        # downloaded. Currently we must download them, so the checkbox
        # to let the user choose has been temporarily removed.
        # load_geometries = self.dlg.ui.load_geometries_chk.isChecked()
        load_geometries = True
        msg = ("Loading socioeconomic data from the OpenQuake "
               "Platform...")
        # Retrieve the indices selected by the user
        indices_list = []
        project_definition = copy.deepcopy(PROJECT_TEMPLATE)
        svi_themes = project_definition[
            'children'][1]['children']
        known_themes = []
        with WaitCursorManager(msg, self.svir.iface):
            while self.dlg.ui.list_multiselect.selected_widget.count() > 0:
                item = \
                    self.dlg.ui.list_multiselect.selected_widget.takeItem(0)
                ind_code = item.text().split(':')[0]
                ind_info = self.dlg.indicators_info_dict[ind_code]
                sv_theme = ind_info['theme']
                sv_field = ind_code
                sv_name = ind_info['name']

                import pdb; pdb.set_trace()
                self.svir._add_new_theme(svi_themes,
                                         known_themes,
                                         sv_theme,
                                         sv_name,
                                         sv_field)

                indices_list.append(sv_field)

            # create string for DB query
            indices_string = ",".join(indices_list)

            self.svir.assign_default_weights(svi_themes)

            try:
                fname, msg = self.sv_downloader.get_data_by_variables_ids(
                    indices_string, load_geometries)
            except SvDownloadError as e:
                self.svir.iface.messageBar().pushMessage(
                    tr("Download Error"),
                    tr(str(e)),
                    level=QgsMessageBar.CRITICAL)
                return
        display_msg = tr(
            "Socioeconomic data loaded in a new layer")
        import pdb; pdb.set_trace()
        self.svir.iface.messageBar().pushMessage(tr("Info"),
                                                 tr(display_msg),
                                                 level=QgsMessageBar.INFO,
                                                 duration=8)
        QgsMessageLog.logMessage(
            msg, 'GEM Social Vulnerability Downloader')
        # don't remove the file, otherwise there will be concurrency
        # problems

        # TODO: Check if we actually want to avoid importing geometries
        if load_geometries:
            uri = ('file://%s?delimiter=,&crs=epsg:4326&skipLines=25'
                   '&trimFields=yes&wktField=geometry' % fname)
        else:
            uri = ('file://%s?delimiter=,&skipLines=25'
                   '&trimFields=yes' % fname)
        # create vector layer from the csv file exported by the
        # platform (it is still not editable!)
        vlayer_csv = QgsVectorLayer(uri,
                                    'socioeconomic_data_export',
                                    'delimitedtext')
        import pdb; pdb.set_trace()
        if not load_geometries:
            if vlayer_csv.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(vlayer_csv)
            else:
                raise RuntimeError('Layer invalid')
            layer = vlayer_csv
        else:
            # obtain a in-memory copy of the layer (editable) and
            # add it to the registry
            layer = ProcessLayer(vlayer_csv).duplicate_in_memory(
                'socioeconomic_zonal_layer',
                add_to_registry=True)
        import pdb; pdb.set_trace()
        self.svir.iface.setActiveLayer(layer)
        self.svir.project_definitions[layer.id()] = project_definition
        print "Before emitting signal"
        self.download_done.emit()
        print "Signal emitted"
