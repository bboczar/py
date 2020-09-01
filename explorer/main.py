import sys

from config import configuration
from core.app import App
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    explorer = App(configuration)
    explorer.show()
    explorer.run()
    sys.exit(app.exec_())
