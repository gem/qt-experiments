# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Svir
                                 A QGIS plugin
 OpenQuake Social Vulnerability and Integrated Risk
                              -------------------
        begin                : 2013-10-24
        copyright            : (C) 2013 by GEM Foundation
        email                : devops@openquake.org
 ***************************************************************************/

# Copyright (c) 2013-2014, GEM Foundation.
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
import csv
import copy
import os
import StringIO
import tempfile
from time import sleep
import traceback

from PyQt4.QtCore import QObject, pyqtSignal

from qgis.core import (QgsVectorLayer, QgsMapLayerRegistry, QgsMessageLog)
from qgis.gui import QgsMessageBar

from third_party.requests import Session

from process_layer import ProcessLayer
from globals import PROJECT_TEMPLATE
from utils import (tr, assign_default_weights)

# FIXME Change exposure to sv when app is ready on platform
PLATFORM_EXPORT_SV_THEMES = "/svir/list_themes"
PLATFORM_EXPORT_SV_SUBTHEMES = "/svir/list_subthemes_by_theme"
PLATFORM_EXPORT_SV_NAMES = "/svir/export_variables_info"
PLATFORM_EXPORT_VARIABLES_DATA_BY_IDS = "/svir/export_variables_data_by_ids"


class SvDownloadError(Exception):
    pass


class SvDownloadAborted(Exception):
    pass


class SvDownloader(object):
    def __init__(self, host):
        self.host = host
        self._login = host + '/account/ajax_login'
        self.sess = Session()

    def login(self, username, password):
        session_resp = self.sess.post(self._login,
                                      data={
                                          "username": username,
                                          "password": password
                                      })
        if session_resp.status_code != 200:  # 200 means successful:OK
            error_message = ('Unable to get session for login: %s' %
                             session_resp.content)
            raise SvDownloadError(error_message)

    def get_themes(self):
        page = self.host + PLATFORM_EXPORT_SV_THEMES
        themes = []
        result = self.sess.get(page)
        if result.status_code == 200:
            reader = csv.reader(StringIO.StringIO(result.content))
            themes = reader.next()
        return themes

    def get_subthemes_by_theme(self, theme):
        page = self.host + PLATFORM_EXPORT_SV_SUBTHEMES
        params = dict(theme=theme)
        subthemes = []
        result = self.sess.get(page, params=params)
        if result.status_code == 200:
            reader = csv.reader(StringIO.StringIO(result.content))
            subthemes = reader.next()
        return subthemes

    def get_indicators_info(
            self, name_filter=None, keywords=None, theme=None, subtheme=None):
        page = self.host + PLATFORM_EXPORT_SV_NAMES
        params = dict(name=name_filter,
                      keywords=keywords,
                      theme=theme,
                      subtheme=subtheme)
        result = self.sess.get(page, params=params)
        indicators_info = {}
        if result.status_code == 200:
            reader = csv.reader(StringIO.StringIO(result.content))
            header = None
            for row in reader:
                if row[0].startswith('#'):
                    continue
                if not header:
                    header = row
                    continue
                code = row[0]
                indicators_info[code] = dict()
                indicators_info[code]['name'] = row[1].decode('utf-8')
                indicators_info[code]['theme'] = row[2].decode('utf-8')
                indicators_info[code]['subtheme'] = row[3].decode('utf-8')
                indicators_info[code]['description'] = row[4].decode('utf-8')
                indicators_info[code]['measurement_type'] = \
                    row[5].decode('utf-8')
                indicators_info[code]['source'] = row[6].decode('utf-8')
                indicators_info[code]['aggregation_method'] = \
                    row[7].decode('utf-8')
                indicators_info[code]['keywords_str'] = row[8].decode('utf-8')
                # names.append(indicators_main_info[code])
        return indicators_info


class SvDownloaderWorker(QObject):
    def __init__(self, svir, sv_downloader, dlg):
        QObject.__init__(self)
        self.svir = svir
        self.sv_downloader = sv_downloader
        self.dlg = dlg
        self.processed = 0
        self.percentage = 0
        self.is_aborted = False

    def fake_run(self):

        print self.get_data_by_variables_ids('ENVDIPINP', True)
        # total = 2
        # for i in range(total):
        #     if self.is_aborted:
        #         raise SvDownloadAborted
        #     sleep(1)
        #     progr = i * 100 / total
        #     self.progress.emit(progr)

    def abort(self):
        self.is_aborted = True

    def update_status(
            self, message, title='Info', level=QgsMessageBar.INFO, duration=0):
        # self.status.emit(message, title, level, duration)
        self.status.emit(message)

    def run(self):
        try:
            #self.fake_run()
            self._run()
            self.update_status('Task done')
            self.finished.emit(True)
        except Exception:
            import traceback
            self.error.emit(traceback.format_exc())
            self.finished.emit(False)

    def _run(self):
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
        while self.dlg.ui.list_multiselect.selected_widget.count() > 0:
            item = \
                self.dlg.ui.list_multiselect.selected_widget.takeItem(0)
            ind_code = item.text().split(':')[0]
            ind_info = self.dlg.indicators_info_dict[ind_code]
            sv_theme = ind_info['theme']
            sv_field = ind_code
            sv_name = ind_info['name']

            self.svir._add_new_theme(svi_themes,
                                     known_themes,
                                     sv_theme,
                                     sv_name,
                                     sv_field)

            indices_list.append(sv_field)

        # create string for DB query
        indices_string = ",".join(indices_list)

        assign_default_weights(svi_themes)

        try:
            fname = self.get_data_by_variables_ids(
                indices_string, load_geometries)
            print fname
        except SvDownloadError as e:
            self.update_status(
                title=tr("Download Error"),
                message=tr(str(e)),
                level=QgsMessageBar.CRITICAL)
            return
        display_msg = tr(
            "Socioeconomic data loaded in a new layer")
        self.update_status(message=tr(display_msg))
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
        self.svir.iface.setActiveLayer(layer)
        self.svir.project_definitions[layer.id()] = project_definition

    def get_data_by_variables_ids(self, sv_variables_ids, load_geometries):
        page = self.sv_downloader.host + PLATFORM_EXPORT_VARIABLES_DATA_BY_IDS
        params = dict(sv_variables_ids=sv_variables_ids,
                      export_geometries=load_geometries)
        result = self.sv_downloader.sess.get(page, params=params, stream=True)
        if result.status_code == 200:
            content_length = int(result.headers.get('content-length'))
            print content_length
            # save csv on a temporary file
            fd, fname = tempfile.mkstemp(suffix='.csv')
            os.close(fd)
            # All the fields of the csv file will be considered as text fields
            # unless a .csvt file with the same name as the .csv file is used
            # to specify the field types.
            # For the type descriptor, use the same name as the csv file
            fname_types = fname.split('.')[0] + '.csvt'
            # We expect iso, country_name, v1, v2, ... vn
            # Count variables ids
            sv_variables_count = len(sv_variables_ids.split(','))
            # build the string that describes data types for the csv
            types_string = '"String","String"' + ',"Real"' * sv_variables_count
            partial_data_length = 0
            if load_geometries:
                types_string += ',"String"'
            with open(fname_types, 'w') as csvt:
                csvt.write(types_string)
            with open(fname, 'w') as csv:
                for partial_data in result.iter_content(chunk_size=512):
                    if self.is_aborted:
                        raise SvDownloadAborted
                    partial_data_length += len(partial_data)
                    csv.write(partial_data)
                    perc_done = int(100 * partial_data_length / content_length)
                    self.progress.emit(perc_done)
            return fname
        else:
            raise SvDownloadError(result.content)

    progress = pyqtSignal(int)
    status = pyqtSignal([str],
                        [str, str],
                        [str, str, int],
                        [str, str, int, int])
    error = pyqtSignal(str)
    killed = pyqtSignal()
    finished = pyqtSignal(bool)
