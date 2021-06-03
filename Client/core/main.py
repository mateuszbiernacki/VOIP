import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import Client.gui.forgot_password_window as forgot_password_window
import Client.gui.friend_request as friend_request
import Client.gui.log_reg_window as log_window
import Client.gui.main_view as main_window
import Client.gui.response_window as response_window
import Client.gui.settings_window as settings_window
from connector import Connector


class Session:
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

    _friend_req_dialog = QtWidgets.QDialog()
    friend_req_ui = friend_request.Ui_Dialog()
    friend_req_ui.setupUi(_friend_req_dialog)

    _main_window = QtWidgets.QMainWindow()
    ui = main_window.Ui_MainWindow()
    ui.setupUi(_main_window)

    @staticmethod
    def start_session():

        def show_response_dialog(short, long):
            Session.response_ui.short_label.setText(short)
            Session.response_ui.long_label.setText(long)
            Session._response_dialog.show()

        def friend_request_dialog(friend_login):
            Session.friend_req_ui.friend_login_label.setText(friend_login)
            Session._friend_req_dialog.show()

        timer = QTimer()

        def check_message_queue():
            data_from_server = Session._connector.get_message()
            if data_from_server['short'] == 's_inv_to_friends':
                friend_request_dialog(data_from_server['friend_login'])
            elif data_from_server['short'] == 'new_friend':
                list_of_friends = Session._connector.get_list_of_friends()['list_of_friends']
                Session.ui.list_of_friends.clear()
                for friend in list_of_friends:
                    Session.ui.list_of_friends.addItem(friend)

        timer.timeout.connect(check_message_queue)

        def press_login_button():
            response = Session._connector.log_in(Session.login_ui.log_line_login.text(),
                                                 Session.login_ui.log_line_password.text())
            if response["short"] == "OK":
                Session._connector.login = Session.login_ui.log_line_login.text()
                Session._connector.set_token(response["token"])
                list_of_friends = Session._connector.get_list_of_friends()['list_of_friends']
                Session.ui.list_of_friends.clear()
                for friend in list_of_friends:
                    Session.ui.list_of_friends.addItem(friend)
                Session._main_window.show()
                Session._login_dialog.hide()
                timer.start(999)
            else:
                show_response_dialog(response["short"], response["long"])

        Session.login_ui.button_log.clicked.connect(press_login_button)

        def press_register_button():
            response = Session._connector.registration(Session.login_ui.reg_line_login.text(),
                                                       Session.login_ui.reg_line_password.text(),
                                                       Session.login_ui.reg_line_email.text())
            show_response_dialog(response["short"], response["long"])

        Session.login_ui.button_reg.clicked.connect(press_register_button)

        def press_settings_button():
            Session.settings_ui.ip_line.setText(Session._connector.server_ip)
            Session.settings_ui.port_line.setText(str(Session._connector.port))
            Session._settings_dialog.show()

        Session.login_ui.button_settings.clicked.connect(press_settings_button)

        def set_server_data():
            Session._connector.server_ip = Session.settings_ui.ip_line.text()
            try:
                Session._connector.port = int(Session.settings_ui.port_line.text())
            except ValueError:
                Session._connector.port = 2137
            print(Session._connector.server_ip)

        Session.settings_ui.buttonBox.accepted.connect(set_server_data)

        def logout_button():
            response = Session._connector.log_out()
            if response["short"] == "OK":
                Session._main_window.hide()
                Session._login_dialog.show()
                timer.stop()
            show_response_dialog(response["short"], response["long"])

        Session.ui.log_out_button.clicked.connect(logout_button)

        def forgot_password_button():
            Session._forgot_pass_dialog.show()

        Session.login_ui.button_forgot_password.clicked.connect(forgot_password_button)

        def forgot_password_send_email():
            response = Session._connector.forgot_password(Session.forgot_pass_ui.login_input_line.text())
            show_response_dialog(response['short'], response['long'])

        Session.forgot_pass_ui.send_code_button.clicked.connect(forgot_password_send_email)

        def change_password_button():
            response = Session._connector.change_password(Session.forgot_pass_ui.login_input_line.text(),
                                                          int(Session.forgot_pass_ui.code_input_line.text()),
                                                          Session.forgot_pass_ui.new_password_line.text())
            show_response_dialog(response['short'], response['long'])

        Session.forgot_pass_ui.check_code_button.clicked.connect(change_password_button)

        def delete_friend_button():
            friend_login = Session.ui.list_of_friends.item(Session.ui.list_of_friends.currentRow()).text()
            response = Session._connector.delete_friend(friend_login)
            list_of_friends = Session._connector.get_list_of_friends()['list_of_friends']
            Session.ui.list_of_friends.clear()
            for friend in list_of_friends:
                Session.ui.list_of_friends.addItem(friend)
            show_response_dialog(response["short"], response["long"])

        Session.ui.delete_friend_list_buton.clicked.connect(delete_friend_button)

        def invite_friend_button():
            response = Session._connector.invite_friend(Session.ui.line_friend_to_invite.text())
            if response['short'] == 'OK':
                Session.ui.line_friend_to_invite.clear()
            show_response_dialog(response["short"], response["long"])

        Session.ui.send_invite_button.clicked.connect(invite_friend_button)

        def accept_friends_invite():
            response = Session._connector.accept_invite(Session.friend_req_ui.friend_login_label.text())
            if response['short'] != 'OK':
                show_response_dialog(response['short'], response['long'])

        Session.friend_req_ui.accept_buton.clicked.connect(accept_friends_invite)

        Session._login_dialog.show()
        sys.exit(Session.app.exec_())


if __name__ == '__main__':
    Session.start_session()
