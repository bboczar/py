import logging
import os

from datetime import datetime
from ui.ui_app import Ui_MainWindow

from PyQt5 import QtWidgets


class App(QtWidgets.QMainWindow):
    def __init__(self, configuration):
        QtWidgets.QWidget.__init__(self, parent=None)

        self._configuration = configuration

        self._setup_environment()
        self._setup_logger()
        self._setup_components()

    #
    # SETUP
    #

    def _setup_environment(self):
        try:
            os.mkdir('logs')
        except FileExistsError:
            pass

    def _setup_logger(self):
        self.logger = logging.getLogger('Logger')
        file_handler = logging.FileHandler('logs\{:%Y-%m-%d %H-%M-%S}.log'.format(datetime.now()))
        file_handler.setLevel(self._configuration.logging['file_level'])
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._configuration.logging['console_level'])

        formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.setLevel(self._configuration.logging['overall_level'])
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info('Logger ready.')

    def _setup_components(self):
        self._create_ui()

    def _create_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    #
    # Interface
    #

    def run(self):
        self.logger.info('It works.')
