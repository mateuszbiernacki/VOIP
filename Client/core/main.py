import Client.gui.log_reg_window as log_window
import Client.gui.main_view as main_window
import Client.gui.response_window as response_window
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from connector import Connector


class Session:

    @staticmethod
    def start_session():
        _connector = Connector()

        app = QtWidgets.QApplication(sys.argv)

        _login_dialog = QtWidgets.QDialog()
        login_ui = log_window.Ui_Login_Register()
        login_ui.setupUi(_login_dialog)

        _response_dialog = QtWidgets.QDialog()
        response_ui = response_window.Ui_Dialog()
        response_ui.setupUi(_response_dialog)

        _main_window = QtWidgets.QMainWindow()
        ui = main_window.Ui_MainWindow()
        ui.setupUi(_main_window)

        def press_login_button():
            response = _connector.log_in(login_ui.log_line_login.text(), login_ui.log_line_password.text())
            if response["short"] == "OK":
                _connector.set_token(response["token"])
                _main_window.show()
                _login_dialog.hide()
            else:
                response_ui.short_label.setText(response["short"])
                response_ui.long_label.setText(response["long"])
                _response_dialog.show()

        login_ui.button_log.clicked.connect(press_login_button)

        _login_dialog.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    Session.start_session()
