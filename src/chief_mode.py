from PyQt6.QtWidgets import QStackedWidget

from src.mode_base import Mode
from PyQt6.QtCore import pyqtSignal

from views.dashboard_chief import ChiefDashboardWindow
from views.appoint import AppointWindow

from src.database.chiefFunc import *
from datetime import datetime

class ChiefMode(Mode):

    def __init__(self, stack: QStackedWidget, name:str, s_id:int):
        super().__init__(stack)
        self.name = name 
        self.id = s_id
    
    def start(self):
        self.dashboard_view : ChiefDashboardWindow = self.add_view(ChiefDashboardWindow()) # type:ignore
        self.dashboard_view.set_staff_id(self.id)
        self.dashboard_view.set_staff_name(self.name)
        self._update_dash()

        self.appoint_view : AppointWindow = self.add_view(AppointWindow()) # type:ignore

        self._connect_slots()

        self._to_dash()


    def _update_dash(self):
        self.applications = get_pending_reg_requests()
        self.dashboard_view.set_pending_applications(len(self.applications))

    def _connect_slots(self):
        # in cheif mode
        self.dashboard_view.appoint_staff_requested.connect(self._to_appoint)

        self.appoint_view.back_requested.connect(self._to_dash)
        self.appoint_view.application_accepted.connect(lambda n, r: self._accept_staff(n, r))
        self.appoint_view.application_rejected.connect(lambda n, r: self._reject_staff(n, r))
        # self.appoint_view.application_rejected.connect(self.

        self.dashboard_view.logout_requested.connect(
            lambda : self.finished.emit(None)
        )

    def _accept_staff(self, name, role):
        staff_id = get_id_by_name(name)
        accept_requestChief(staff_id)

    def _reject_staff(self, name, role):
        staff_id = get_id_by_name(name)
        reject_requestChief(staff_id)

    def _to_dash(self):
        self._update_dash()
        self.show(self.dashboard_view)

    def _to_appoint(self):
        # TODO: Set appoint rows here
        # TODO: Add dates
        reqs_with_date = [(n, r, "placeholder") 
                            for (n, r) in self.applications]
        self.appoint_view.set_applications(
            reqs_with_date
        )
        self.show(self.appoint_view)