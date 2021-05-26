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

        def show_response_dialog(short, long):
            response_ui.short_label.setText(short)
            response_ui.long_label.setText(long)
            _response_dialog.show()

        def press_login_button():
            response = _connector.log_in(login_ui.log_line_login.text(), login_ui.log_line_password.text())
            if response["short"] == "OK":
                _connector.login = login_ui.log_line_login.text()
                _connector.set_token(response["token"])
                _main_window.show()
                _login_dialog.hide()
            else:
                show_response_dialog(response["short"], response["long"])

        login_ui.button_log.clicked.connect(press_login_button)

        def press_register_button():
            response = _connector.registration(login_ui.reg_line_login.text(),
                                               login_ui.reg_line_password.text(),
                                               login_ui.reg_line_email.text())
            show_response_dialog(response["short"], response["long"])

        login_ui.button_reg.clicked.connect(press_register_button)

        def logout_button():
            response = _connector.log_out()
            if response["short"] == "OK":
                _main_window.hide()
                _login_dialog.show()
            show_response_dialog(response["short"], response["long"])

        ui.log_out_button.clicked.connect(logout_button)

        _login_dialog.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    Session.start_session()
