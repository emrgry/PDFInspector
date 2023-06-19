from PySide6 import QtCore, QtWidgets, QtGui
from screens.managerScreen import ManagerScreen
from firebase import Firebase

class InitScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.preferences_path = "preferences.txt"
        self.selected_file = ""
        self.exam_type = ""
        self.exam_ref = ""
        self.new_window = None

        self.exam_type_dict = {}

        self.firebase = Firebase()
        
        self.setWindowTitle("Select PDF")
        
        central_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.label = QtWidgets.QLabel("Choose file you want to inspect")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)


        self.button = QtWidgets.QPushButton("Start Inspect")
        self.button.clicked.connect(self.open_new_window)
        
        self.fileButton = QtWidgets.QPushButton("Dosya Seç")
        # self.fileButton.setFixedWidth(200)
        # self.fileButton.setAlignment(QtCore.Qt.AlignCenter)
        self.fileButton.clicked.connect(self.select_file)
        self.layout.addWidget(self.fileButton)

        nameInputArea = QtWidgets.QHBoxLayout()
        self.layout.addLayout(nameInputArea)

        nameLabel = QtWidgets.QLabel("Exam Name")
        self.nameInput = QtWidgets.QLineEdit()
        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.activated.connect(self.handleActivated)
        self.addItems()
        

        nameInputArea.addWidget(nameLabel)
        nameInputArea.addWidget(self.nameInput)
        nameInputArea.addWidget(self.combo_box)

        answerInputArea = QtWidgets.QHBoxLayout()
        self.layout.addLayout(answerInputArea)

        answerKeyLabel = QtWidgets.QLabel("Answer key page")
        self.answerKeyInput = QtWidgets.QLineEdit()
        self.answerKeyInput.setFixedSize(50, 20)

        answerInputArea.addWidget(answerKeyLabel)
        answerInputArea.addWidget(self.answerKeyInput)
        answerInputArea.addStretch()
        
    
    def open_new_window(self):
        name = self.nameInput.text()
        answer_page = int(self.answerKeyInput.text())
        self.exam_type = self.combo_box.itemText(0)
        self.exam_ref = self.exam_type_dict[self.exam_type]
        self.new_window = ManagerScreen(self.firebase, self.selected_file, self.exam_ref, self.exam_type, name, answer_page)
        self.new_window.show()
        self.hide()
    
    def addItems(self):
        self.exam_type_dict = self.firebase.get_exam_types()
        for key, value in self.exam_type_dict.items():
            self.combo_box.addItem(key)
    
    def handleActivated(self, index):
        selected_item_text = self.combo_box.itemText(index)
        self.exam_type = selected_item_text
        self.exam_ref = self.exam_type_dict[self.exam_type]
    
    
    def closeEvent(self, event):
        if self.new_window is not None and self.new_window.isVisible():
            self.new_window.close()  # Yeni pencereyi kapat
        event.accept()

    def select_file(self):
        file_dialog = QtWidgets.QFileDialog()
        initial_path = self.load_preferences(self.preferences_path)
        file_path, _ = file_dialog.getOpenFileName(self, "Dosya Seç", initial_path)
        if file_path:
            self.label.setText(f"Seçilen Dosya: {file_path}")
            self.save_preferences(self.preferences_path, file_path)
            self.layout.addWidget(self.button)
            self.selected_file = file_path
    
    def load_preferences(self, path):
        try:
            with open(path, "r") as file:
                return file.readline().strip()
        except FileNotFoundError:
            return QtCore.QDir.homePath()

    def save_preferences(self, path, value):
        with open(path, "w") as file:
            file.write(value)