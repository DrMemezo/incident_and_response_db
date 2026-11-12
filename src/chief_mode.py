from PyQt6.QtWidgets import QStackedWidget

from src.mode_base import Mode
from PyQt6.QtCore import pyqtSignal

from views.dashboard_chief import ChiefDashboardWindow
from views.appoint import AppointWindow

from src.database.chiefFunc import *
from datetime import datetime

class ChiefMode(Mode):

    def __init__(self, stack: QStackedWidget, name:str, id:int):
        super().__init__(stack)
        self.name = name 
        self.id = id
    
    def start(self):
        self.dashboard_view : ChiefDashboardWindow = self.add_view(ChiefDashboardWindow()) # type:ignore
        self.dashboard_view.set_staff_id(self.id)
        self.dashboard_view.set_staff_name(self.name)
        # TODO:
        self.dashboard_view.set_pending_applications(0)

        self.appoint_view : AppointWindow = self.add_view(AppointWindow()) # type:ignore


        self._connect_slots()


    def _connect_slots(self):
        self.dashboard_view.appoint_staff_requested.connect(lambda: self._to_appoint())

    
    def _to_appoint(self):
        # TODO: Set appoint rows here
        # TODO: Add dates
        all_reqs = get_pending_reg_requests()
        reqs_with_date = [(n, r, "placeholder") 
                            for (n, r) in all_reqs]
        self.appoint_view.set_applications(
            reqs_with_date
        )
        self.show(self.appoint_view)