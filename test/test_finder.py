import rumps
def hello(sender):
    print(f"Hello from {sender.title}")

app = rumps.App("Hello World")
app.menu = [rumps.MenuItem("Weird Menu Item",callback=hello)]
app.run()