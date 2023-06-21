from PySide6 import QtCore, QtWidgets, QtGui
from firebase import Firebase
from dataType import QuestionData
import cv2

class LeftLayout(QtWidgets.QVBoxLayout):
    def __init__(self, manager, exam_name, exam_type):
        super().__init__()

        self.exam_name = exam_name
        self.exam_type = exam_type
        self.manager = manager
        self.firebase = manager.firebase
        
        self.question_number = 1
        self.answers = {}

        

        ##### left layout
        # get question number
        questionNumberArea = QtWidgets.QHBoxLayout()
        self.addLayout(questionNumberArea)

        questionNumberLabel = QtWidgets.QLabel("QuestionNumber")
        self.questionNumberInput = QtWidgets.QLineEdit()
        self.questionNumberInput.setAlignment(QtCore.Qt.AlignCenter)
        self.questionNumberInput.setFixedSize(50, 20)

        questionNumberArea.addWidget(questionNumberLabel)
        questionNumberArea.addWidget(self.questionNumberInput)

        # get question
        questionArea = QtWidgets.QHBoxLayout()
        self.addLayout(questionArea)

        addImageArea = QtWidgets.QVBoxLayout()

        questionLabel = QtWidgets.QLabel("Question")
        self.questionInput = QtWidgets.QPlainTextEdit()
        imageButton = QtWidgets.QPushButton("Add image")

        self.imageArea = QtWidgets.QHBoxLayout()
        addImageArea.addLayout(self.imageArea)

        imageButton.clicked.connect(lambda: self.createImageArea(self.imageArea))

        self.imageInputLabel = QtWidgets.QLabel("Image url:")
        self.imageUrlLabel = QtWidgets.QLineEdit()
        
        # removeButton = QtWidgets.QPushButton("X")
        # removeButton.clicked.connect(lambda: self.removePressed(imageArea, options))

        questionArea.addLayout(addImageArea)
        addImageArea.addWidget(questionLabel)
        addImageArea.addWidget(imageButton)
        questionArea.addWidget(self.questionInput)

        self.imageArea.addWidget(self.imageInputLabel)
        self.imageArea.addWidget(self.imageUrlLabel)
        self.imageInputLabel.hide()
        self.imageUrlLabel.hide()
    
        # get options
        optionsArea = QtWidgets.QHBoxLayout()
        
        self.addLayout(optionsArea)

        optionsRight = QtWidgets.QVBoxLayout()
        self.optionsLeft = QtWidgets.QVBoxLayout()

        self.optImageArea = QtWidgets.QHBoxLayout()

        self.optImageInputLabel = QtWidgets.QLabel("Image url:")
        self.optImageUrlLabel = QtWidgets.QLineEdit()

        optionsLabel = QtWidgets.QLabel("Options")
        optionButtonLabel = QtWidgets.QPushButton("Add image")

        self.optionsLeft.addWidget(optionsLabel)
        self.optionsLeft.addLayout(self.optImageArea)
        self.optionsLeft.addWidget(optionButtonLabel)
        optionsArea.addLayout(self.optionsLeft)
        optionsArea.addLayout(optionsRight)

        optionAArea = QtWidgets.QHBoxLayout()
        optionBArea = QtWidgets.QHBoxLayout()
        optionCArea = QtWidgets.QHBoxLayout()
        optionDArea = QtWidgets.QHBoxLayout()

        optionsRight.addLayout(optionAArea)
        optionsRight.addLayout(optionBArea)
        optionsRight.addLayout(optionCArea)
        optionsRight.addLayout(optionDArea)

        

        optionA = QtWidgets.QLabel("A")
        optionB = QtWidgets.QLabel("B")
        optionC = QtWidgets.QLabel("C")
        optionD = QtWidgets.QLabel("D")

        optionsAInput = QtWidgets.QLineEdit()
        optionsBInput = QtWidgets.QLineEdit()
        optionsCInput = QtWidgets.QLineEdit()
        optionsDInput = QtWidgets.QLineEdit()

        optionsAInput.setAlignment(QtCore.Qt.AlignCenter)
        optionsBInput.setAlignment(QtCore.Qt.AlignCenter)
        optionsCInput.setAlignment(QtCore.Qt.AlignCenter)
        optionsDInput.setAlignment(QtCore.Qt.AlignCenter)

        optionAArea.addWidget(optionA)
        optionAArea.addWidget(optionsAInput)

        optionBArea.addWidget(optionB)
        optionBArea.addWidget(optionsBInput)

        optionCArea.addWidget(optionC)
        optionCArea.addWidget(optionsCInput)

        optionDArea.addWidget(optionD)
        optionDArea.addWidget(optionsDInput)

        self.lineArrays = [optionsAInput, optionsBInput, optionsCInput, optionsDInput]

        optionButtonLabel.clicked.connect(lambda: self.createImageArea(self.optImageArea, options=self.lineArrays))
        self.optImageArea.addWidget(self.optImageInputLabel)
        self.optImageArea.addWidget(self.optImageUrlLabel)
        self.optImageInputLabel.hide()
        self.optImageUrlLabel.hide()

        # get answer
        answerArea = QtWidgets.QHBoxLayout()
        self.addLayout(answerArea)

        answerLabel = QtWidgets.QLabel("Answer")
        self.answerInput = QtWidgets.QLineEdit()
        self.answerInput.setAlignment(QtCore.Qt.AlignCenter)
        self.answerInput.setFixedSize(50, 20)

        answerArea.addWidget(answerLabel)
        answerArea.addWidget(self.answerInput)
        

        # get description
        descriptionArea = QtWidgets.QHBoxLayout()
        self.addLayout(descriptionArea)

        descriptionLabel = QtWidgets.QLabel("Description")
        self.descriptionInput = QtWidgets.QPlainTextEdit()

        descriptionArea.addWidget(descriptionLabel)
        descriptionArea.addWidget(self.descriptionInput)

        # next button
        self.nextQuestionArea = QtWidgets.QHBoxLayout()
        self.addLayout(self.nextQuestionArea)

        nextButton = QtWidgets.QPushButton("Next Question")
        nextButton.setFixedWidth(100)
        nextButton.clicked.connect(self.nextPressed)
        self.nextQuestionArea.addStretch()
        self.nextQuestionArea.addWidget(nextButton)

        self.sendButton = QtWidgets.QPushButton("Send")
        self.sendButton.setFixedWidth(100)
        self.sendButton.clicked.connect(self.sendPressed)
        self.nextQuestionArea.addStretch()
        
    def fill_question_area(self, question, options):
        self.questionInput.setPlainText(question)
        self.lineArrays[0].setText(options[0])
        self.lineArrays[1].setText(options[1])
        self.lineArrays[2].setText(options[2])
        self.lineArrays[3].setText(options[3])
    
    def init_first_question(self):
        self.answers = self.manager.get_answers()
        self.questionNumberInput.setText(str(self.question_number))
        self.answerInput.setText(self.answers[str(self.question_number)])

    def sendPressed(self):
        self.manager.sendFirebase()

    def nextPressed(self):
        if len(self.answers) == self.question_number:
            self.nextQuestionArea.addWidget(self.sendButton)
            return

        q_num = self.questionNumberInput.text()
        quest = self.questionInput.toPlainText()
        q_image = self.imageUrlLabel.text()
        options = {
            "a":self.lineArrays[0].text(),
            "b":self.lineArrays[1].text(),
            "c":self.lineArrays[2].text(),
            "d":self.lineArrays[3].text(),
        }
        opt_image = self.optImageUrlLabel.text()
        ans = self.answerInput.text()
        desc = self.descriptionInput.toPlainText()
        self.manager.append_array(q_num,quest,q_image,options,opt_image,ans,desc)
        
        self.question_number += 1
        self.questionNumberInput.setText(str(self.question_number))
        self.answerInput.setText(self.answers[str(self.question_number)])
        self.cleanInputs()
    
    def cleanInputs(self):
        self.questionInput.setPlainText('')
        self.imageUrlLabel.setText('')
        self.lineArrays[0].setText('')
        self.lineArrays[1].setText('')
        self.lineArrays[2].setText('')
        self.lineArrays[3].setText('')
        self.optImageUrlLabel.setText('')
        self.descriptionInput.setPlainText('')
        self.removePressed()

    
    def uploadFirebaseImage(self,options=None):
        self.cvWindow = cv2.namedWindow('Select')
        numpy_image = self.manager.get_numpy_image()
        r = cv2.selectROI("Select", numpy_image)
        selected_region = numpy_image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        file_name = 'temp/'
        if options:
            file_name += self.exam_name + str(self.question_number) + "-option.png"
        else:
            file_name += self.exam_name + str(self.question_number) + "-question.png"
        cv2.imwrite(file_name, selected_region)

        url = self.firebase.uploadImage(file_name)
        cv2.destroyAllWindows()
        return url

    def createImageArea(self, parent, options=None):
        url = self.uploadFirebaseImage(options)


        if options:
            self.optImageInputLabel.show()
            self.optImageUrlLabel.show()
            options[0].setText('A')
            options[1].setText('B')
            options[2].setText('C')
            options[3].setText('D')
            self.optImageUrlLabel.setText(url)
        else:
            self.imageInputLabel.show()
            self.imageUrlLabel.show()
            self.imageUrlLabel.setText(url)
            


    
    def removePressed(self):
        self.imageUrlLabel.setText('')
        self.optImageUrlLabel.setText('')
        self.imageInputLabel.hide()
        self.imageUrlLabel.hide()
        self.optImageInputLabel.hide()
        self.optImageUrlLabel.hide()
        # while area.count():
        #     item = area.takeAt(0)
        #     widget = item.widget()
        #     if widget:
        #         widget.deleteLater()
        # self.update()

        # if options:
        #     options[0].setText('')
        #     options[1].setText('')
        #     options[2].setText('')
        #     options[3].setText('')