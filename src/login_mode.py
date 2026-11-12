from src.mode_base import Mode

from views.login import LoginWindow
from views.register import RegisterWindow
from views.register_denied import RegisterDeniedWindow
from views.register_submitted import RegisterSubmittedWindow

from src.database.registration_functions import *
from PyQt6.QtCore import pyqtSignal

class LoginMode(Mode):
    
    def start(self):
    
        self.login_view: LoginWindow = self.add_view(LoginWindow()) #type:ignore
        self.register_view: RegisterWindow = self.add_view(RegisterWindow())#type:ignore
        self.register_denied_view = self.add_view(RegisterDeniedWindow())#type:ignore
        self.register_accepted_view = self.add_view(RegisterSubmittedWindow())#type:ignore

        self._connect_slots()

        self._to_login()

    def _connect_slots(self):
        self.login_view.register_requested.connect(lambda : self._to_register())
        self.register_view.login_requested.connect(lambda : self._to_login())

        self.register_view.application_submitted.connect( lambda name, passw, role : self._add_registered(name, passw, role))   
        self.login_view.login_requested.connect(lambda name, passw : self.attempt_login(name, passw))    

    def _to_register(self):
        self.show(self.register_view)

    def _to_login(self):
        self.show(self.login_view) 

    def _add_registered(self, name, passw, role):
       if not check_for_same_name(name):
           self.register_view.show_error("This staff already exists!")
           return

       submit_request(name, role, passw)

    def attempt_login(self, name, passw):
        result = get_staff_info(name, passw) # If the user is an accepted member of staff
        if not result:
            self.login_view.show_error("Invalid Login!")
            return
        s_id, _, title = result
        self.finished.emit({"s_id": int(s_id), "name": name, "title": title})
