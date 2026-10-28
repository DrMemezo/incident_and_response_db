"""
flow_demo.py - Minimal demo of how to model the flow between screens.

Flow implemented here
---------------------

        +-------------------+  register_requested   +-------------------+
        |   LoginWindow     | --------------------> |  RegisterWindow   |
        |   (start screen)  | <-------------------- |                   |
        +-------------------+  (see note below)     +-------------------+
                 ^                                           |
                 |                                           | application_submitted
                 |  back_to_login_requested                  v
                 |                                  +-----------------------+
                 +--------------------------------- | RegisterSubmittedWindow|
                                                    +-----------------------+

(The register form has no "back" button in its .ui file, so the only way back
to login is via the "submitted" screen. Add a button + signal if you want one.)

The pattern
-----------
1. **Windows are "dumb".** Each window only emits signals such as
   ``register_requested`` ("the user wants to register"). None of them imports
   or knows about another window.

2. **One controller owns the flow.** ``AppController`` creates every window,
   connects their signals to its own methods, and decides which window is
   visible. Every transition in the app is therefore in ONE place, and reading
   ``_connect_signals()`` shows the whole flow at a glance.

3. **One navigation method.** All transitions go through ``show_screen()``,
   which hides the current window and shows the next one. If you later want
   animations, a window stack, or a "back" history, you change it there only.

To add a screen: create the window in ``__init__``, connect its signals in
``_connect_signals()``, and call ``show_screen()`` from the handlers.

Run it with:

    python flow_demo.py

(login.py, register_v2.py, register_submitted.py and their .ui files must be in
the same folder.)
"""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from views.login import LoginWindow
from views.register_submitted import RegisterSubmittedWindow
from views.register import RegisterWindow


class AppController:
    """Owns all windows and decides which one is shown.

    This is a plain Python object, not a widget: it has no UI of its own. It
    just wires signals to navigation.
    """

    def __init__(self) -> None:
        # Create every window once, up front. They stay alive (hidden) for the
        # whole program, so form contents are not lost by switching screens.
        # For a large app you could instead create them lazily on first use.
        self.login = LoginWindow()
        self.register = RegisterWindow()
        self.submitted = RegisterSubmittedWindow()

        # The window that is currently visible (None until start() is called).
        self._current: QMainWindow | None = None

        self._connect_signals()

    # ------------------------------------------------------------------ flow
    def _connect_signals(self) -> None:
        """The whole screen flow, in one place.

        Read as: "when <window> emits <signal>, call <handler>".
        """
        # Login screen
        self.login.register_requested.connect(self._on_register_requested)
        self.login.login_requested.connect(self._on_login_requested)

        # Register screen
        self.register.application_submitted.connect(self._on_application_submitted)

        # "Submitted" confirmation screen
        self.submitted.back_to_login_requested.connect(self._on_back_to_login)

    # ------------------------------------------------------------ navigation
    def start(self) -> None:
        """Show the first screen. Call once after creating the controller."""
        self.show_screen(self.login)

    def show_screen(self, target: QMainWindow) -> None:
        """Hide the current window and show ``target`` in its place.

        The new window is centred on the old one, so the user's eye does not
        have to hunt for it (the screens have different sizes).
        """
        previous = self._current

        if previous is not None:
            # Centre the target on the window we are leaving.
            geometry = target.geometry()
            geometry.moveCenter(previous.geometry().center())
            target.setGeometry(geometry)
            previous.hide()

        target.show()
        target.raise_()
        target.activateWindow()
        self._current = target

    # -------------------------------------------------------------- handlers
    def _on_register_requested(self) -> None:
        """Login -> Register."""
        self.show_screen(self.register)

    def _on_login_requested(self, name: str, password: str) -> None:
        """Login screen submitted credentials.

        This demo has no user database, so it only reports what it received.
        In a real app you would verify the credentials here and then either
        ``show_screen()`` the main window or call ``self.login.show_error()``.
        """
        self.login.clear_password()
        QMessageBox.information(
            self.login,
            "Demo",
            f"Login requested for '{name}', with password: {password}.\n\n"
            "This demo has no user database, so nobody is actually logged in.",
        )

    def _on_application_submitted(self, name: str, password: str, role: str) -> None:
        """Register -> Submitted.

        A real app would save the application here (hashing the password).
        """
        print(f"Application received: {name} as {role}, with pw: {password}")

        # Personalise the confirmation message using the submitted data.
        self.submitted.set_message(
            f"Thanks, {name}! The Chief will review your application for "
            f"{role}. You will be able to log in once it has been accepted."
        )

        # Clear the form so it is empty if the user comes back to it later.
        self.register.reset_form()
        self.show_screen(self.submitted)

    def _on_back_to_login(self) -> None:
        """Submitted -> Login."""
        self.login.reset_form()
        self.show_screen(self.login)


def main() -> None:
    app = QApplication(sys.argv)

    # Keep a reference to the controller for the lifetime of the program.
    # If it were garbage-collected, its signal connections would disappear.
    controller = AppController()
    controller.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
