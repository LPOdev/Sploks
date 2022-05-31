from PyQt5 import QtCore, QtWidgets



# A message box that closes itself after a certain amount of time.
class TimerMessageBox(QtWidgets.QMessageBox):
    def __init__(self, timeout=3, msg_text="No message", parent=None):
        """
        Display a message box with a progress bar for a set amount of time
        
        :param timeout: The time in seconds that the message box will be shown, defaults to 3 (optional)
        :param msg_text: The text that will be displayed in the dialog box, defaults to No message
        (optional)
        :param parent: The parent of the dialog
        """
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle("wait")
        self.time_to_wait = timeout
        self.setText(msg_text)
        self.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        """
        The function is a method of the class. 
        It takes no arguments (except self) and returns nothing. 
        called when the class is instantiated. 
        It changes the content of the window. 
        It waits one second and then closes the window.
        """
        """
        The function is a method of the class. 
        It takes no arguments (except self) and returns nothing. 
        called when the class is instantiated. 
        It changes the content of the window. 
        It waits one second and then closes the window
        """
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        """
        When the user closes the window, the timer will stop
        
        :param event: the event that caused the window to close
        """
        self.timer.stop()
        event.accept()