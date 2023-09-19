import rumps
from pynput import keyboard
import tkinter as tk


class MyStatusBarApp(rumps.App):
    def __init__(self):
        super(MyStatusBarApp, self).__init__(
            "My App", icon="../notice.png", title="健哥～～～")
        self.menu = [rumps.MenuItem("自动获取禅道信息", callback=self.start_listening),
                     rumps.MenuItem("立即获取禅道信息", callback=self.stop_listening),
                     rumps.MenuItem("登录获取 token", callback=self.login_get_token)]
        self.loop_thread = None
        self.is_running = False

    def login_get_token(self, _):
        print("login_get_token")

    def start_listening(self, _):
        if not self.listener:
            self.listener = keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()

    def stop_listening(self, _):
        if self.listener:
            self.listener.stop()
            self.listener = None




if __name__ == "__main__":
    app = MyStatusBarApp()
    app.run()
