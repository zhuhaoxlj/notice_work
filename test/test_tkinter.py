import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录窗口")
        self.setGeometry(100, 100, 400, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建用户名标签和输入框
        self.username_label = QLabel("用户名:")
        self.username_entry = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)

        # 创建密码标签和输入框
        self.password_label = QLabel("密码:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)  # 使密码框显示星号
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)

        # 创建登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.on_login_button_click)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def on_login_button_click(self):
        # 获取用户名和密码输入框的文本
        username = self.username_entry.text()
        password = self.password_entry.text()

        # 打印用户名和密码
        print("用户名:", username)
        print("密码:", password)

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()