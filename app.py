from ui import UI


class App:
    def __init__(self):
        self._ui = UI()

    # PUBLIC METHODS
    def start(self):
        self._ui.mainloop()
