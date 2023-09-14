import rumps

class MyMacApp(rumps.App):
    def __init__(self):
        super(MyMacApp, self).__init__("My App Name")
        # 设置应用程序图标
        self.icon = "/Users/markgosling/Documents/100-Project/02-Python/MyScript/notice.png"
        self.menu = [
            rumps.MenuItem("Show Notification", callback=self.show_notification),
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]

    def show_notification(self, _):
        rumps.notification(title="My Notification",
                           subtitle="This is a custom notification",
                           message="Hello, macOS!",
                           sound=True)

    def quit_app(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    app = MyMacApp()
    app.run()
    app.show_notification()