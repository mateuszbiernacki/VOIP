import Client.gui.log_reg_window as log_window
import Client.gui.main_view as main_window
import Client.gui.response_window as response_window
import Client.gui.settings_window as settings_window
import Client.gui.forgot_password_window as forgot_password_window
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

        _settings_dialog = QtWidgets.QDialog()
        settings_ui = settings_window.Ui_Dialog()
        settings_ui.setupUi(_settings_dialog)

        _forgot_pass_dialog = QtWidgets.QDialog()
        forgot_pass_ui = forgot_password_window.Ui_Dialog()
        forgot_pass_ui.setupUi(_forgot_pass_dialog)

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
                list_of_friends = _connector.get_list_of_friends()['list_of_friends']
                ui.list_of_friends.clear()
                for friend in list_of_friends:
                    ui.list_of_friends.addItem(friend)
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

        def press_settings_button():
            settings_ui.ip_line.setText(_connector.server_ip)
            settings_ui.port_line.setText(str(_connector.port))
            _settings_dialog.show()

        login_ui.button_settings.clicked.connect(press_settings_button)

        def set_server_data():
            _connector.server_ip = settings_ui.ip_line.text()
            try:
                _connector.port = int(settings_ui.port_line.text())
            except ValueError:
                _connector.port = 2137
            print(_connector.server_ip)

        settings_ui.buttonBox.accepted.connect(set_server_data)

        def logout_button():
            response = _connector.log_out()
            if response["short"] == "OK":
                _main_window.hide()
                _login_dialog.show()
            show_response_dialog(response["short"], response["long"])

        ui.log_out_button.clicked.connect(logout_button)

        def forgot_password_button():
            _forgot_pass_dialog.show()

        login_ui.button_forgot_password.clicked.connect(forgot_password_button)

        def forgot_password_send_email():
            response = _connector.forgot_password(forgot_pass_ui.login_input_line.text())
            show_response_dialog(response['short'], response['long'])

        forgot_pass_ui.send_code_button.clicked.connect(forgot_password_send_email)

        def change_password_button():
            response = _connector.change_password(forgot_pass_ui.login_input_line.text(),
                                                  int(forgot_pass_ui.code_input_line.text()),
                                                  forgot_pass_ui.new_password_line.text())
            show_response_dialog(response['short'], response['long'])

        forgot_pass_ui.check_code_button.clicked.connect(change_password_button)

        def delete_friend_button():
            friend_login = ui.list_of_friends.item(ui.list_of_friends.currentRow()).text()
            response = _connector.delete_friend(friend_login)
            list_of_friends = _connector.get_list_of_friends()['list_of_friends']
            ui.list_of_friends.clear()
            for friend in list_of_friends:
                ui.list_of_friends.addItem(friend)
            show_response_dialog(response["short"], response["long"])

        ui.delete_friend_list_buton.clicked.connect(delete_friend_button)

        _login_dialog.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    Session.start_session()
