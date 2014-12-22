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
import os
import StringIO
import tempfile
from time import sleep

from PyQt4.QtCore import QObject, pyqtSignal

from qgis.core import QgsVectorLayer

from third_party.requests import Session

from process_layer import ProcessLayer
from globals import DEBUG

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
        themes = self.get_items()
        return themes

    def get_subthemes_by_theme(self, theme):
        subthemes = self.get_items(theme)
        return subthemes

    def get_items(self, theme=None):
        # return the list of themes if theme is not provided,
        # otherwise return the list of subthemes corresponding to that theme
        params = dict()
        items = []
        if theme is None:
            page = self.host + PLATFORM_EXPORT_SV_THEMES
        else:
            page = self.host + PLATFORM_EXPORT_SV_SUBTHEMES
            params['theme'] = theme
        result = self.sess.get(page, params=params)
        if result.status_code == 200:
            reader = csv.reader(StringIO.StringIO(result.content))
            items = reader.next()
        return items

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
    def __init__(self, sv_downloader, indicators_str, load_geometries):
        QObject.__init__(self)
        self.sv_downloader = sv_downloader
        self.indicators_str = indicators_str
        self.load_geometries = load_geometries
        self.processed = 0
        self.percentage = 0
        self.is_aborted = False
        self.downloaded_csv = None
        self.layer = None

    def abort(self):
        """
        Sets a flag to abort the download
        """
        self.is_aborted = True

    def check_aborted(self):
        """
        checks if the abort flag is set and if yes raises SvDownloadAborted
        :raises: SvDownloadAborted
        """
        if self.is_aborted:
            raise SvDownloadAborted

    def run(self):
        """
        Start the downloader and emits finished(bool) and error(str) if needed
        """
        try:
            # self.fake_run()
            self.download_data()
            self.check_aborted()
            self.make_qgis_layer()
            self.check_aborted()
            self.finished.emit(True)
        except SvDownloadAborted:
            self.finished.emit(False)
        except Exception:
            self.abort()
            import traceback
            self.error.emit(traceback.format_exc())
            self.finished.emit(False)

    def download_data(self):
        """
        Downloads data from the plattform creating a CSV file
        in self.downloaded_csv

        :raises SvDownloadError
        """
        page = self.sv_downloader.host + PLATFORM_EXPORT_VARIABLES_DATA_BY_IDS
        params = dict(sv_variables_ids=self.indicators_str,
                      export_geometries=self.load_geometries)
        self.progressText.emit('Querying the Socioeconomic Database')
        result = self.sv_downloader.sess.get(page, params=params, stream=True)
        self.check_aborted()
        if result.status_code == 200:
            content_length = int(result.headers.get('content-length'))
            # bytes to Mb
            self.progressTogglePercent.emit(True)
            self.progressText.emit(
                'Downloading %sMb' % (content_length/1024/1024))
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
            sv_variables_count = len(self.indicators_str.split(','))
            # build the string that describes data types for the csv
            types_string = '"String","String"' + ',"Real"' * sv_variables_count
            partial_data_length = 0
            if self.load_geometries:
                types_string += ',"String"'
            with open(fname_types, 'w') as csvt:
                csvt.write(types_string)
            with open(fname, 'w') as csv:
                for partial_data in result.iter_content(chunk_size=512):
                    self.check_aborted()
                    partial_data_length += len(partial_data)
                    csv.write(partial_data)
                    perc_done = int(100 * partial_data_length / content_length)
                    self.progress.emit(perc_done)
            self.downloaded_csv = fname
        else:
            raise SvDownloadError(result.content)

        # All went well
        if DEBUG:
            print 'File downloaded at: %s' % self.downloaded_csv

    def make_qgis_layer(self):
        """
        Creates QgsVectorLayer from the downloaded CSV storing it in self.layer

        :raises RuntimeError, TypeError
        """
        self.progressTogglePercent.emit(False)
        self.progressText.emit('Creating QGIS layer')

        # count top lines in the csv starting with '#'
        with open(self.downloaded_csv) as f:
            lines_to_skip_count = 0
            for line in f:
                li = line.strip()
                if li.startswith('#'):
                    lines_to_skip_count += 1
                else:
                    break

        if DEBUG:
            print "%s rows will be skipped from the CSV" % lines_to_skip_count

        if self.load_geometries:
            uri = ('file://%s?delimiter=,&crs=epsg:4326&skipLines=%s'
                   '&trimFields=yes&wktField=geometry' % (self.downloaded_csv,
                                                          lines_to_skip_count))
        else:
            uri = ('file://%s?delimiter=,&skipLines=%s'
                   '&trimFields=yes' % (self.downloaded_csv,
                                        lines_to_skip_count))

        if DEBUG:
            print 'Reading CSV using %s' % uri
        # create vector layer from the csv file exported by the
        # platform (it is still not editable!)
        vlayer_csv = QgsVectorLayer(uri,
                                    'socioeconomic_data_export',
                                    'delimitedtext')
        self.check_aborted()
        if self.load_geometries:
            # obtain a in-memory copy of the layer (editable) and
            # add it to the registry
            layer = ProcessLayer(vlayer_csv).duplicate_in_memory(
                'socioeconomic_zonal_layer')
        else:
            if vlayer_csv.isValid():
                layer = vlayer_csv
            else:
                raise RuntimeError('CSV Layer invalid')

        self.layer = layer

    # Define own signals
    progress = pyqtSignal(int)
    progressText = pyqtSignal(str)
    progressTogglePercent = pyqtSignal(bool)
    status = pyqtSignal(str)
    error = pyqtSignal(str)
    killed = pyqtSignal()
    finished = pyqtSignal(bool)

    # for debugging
    def fake_run(self):
        total = 5
        for i in range(1, total+1):
            self.check_aborted()
            sleep(1)
            progr = i * 100 / total
            self.progress.emit(progr)
