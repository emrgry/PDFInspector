from PySide6 import QtCore, QtWidgets, QtGui
import cv2
import numpy as np
import pytesseract
import copy
import re

class RightLayout(QtWidgets.QVBoxLayout):
    def __init__(self, manager):
        super().__init__()

        self.manager = manager
        self.current_page = 1
        self.numpy_image = None
        self.pix_image_shape = None
        

        # next button
        selectQuestionArea = QtWidgets.QHBoxLayout()
        self.addLayout(selectQuestionArea)

        nextButton = QtWidgets.QPushButton("Select Question")
        nextButton.setFixedWidth(120)
        nextButton.clicked.connect(self.selectPressed)
        selectQuestionArea.addWidget(nextButton)
        selectQuestionArea.addStretch()

        checkbox = QtWidgets.QCheckBox("Checkbox")
        checkbox.stateChanged.connect(self.checkboxStateChanged)
        selectQuestionArea.addWidget(checkbox)

        self.imageLabel = QtWidgets.QLabel()
        # self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # self.imageLabel.setScaledContents(True)

        bottomHBox = QtWidgets.QHBoxLayout()
        prevButton = QtWidgets.QPushButton("<")
        prevButton.setFixedWidth(50)
        prevButton.clicked.connect(self.prevPressed)

        nextButton = QtWidgets.QPushButton(">")
        nextButton.setFixedWidth(50)
        nextButton.clicked.connect(self.nextPressed)

        self.pageInput = QtWidgets.QLineEdit()
        self.pageInput.setFixedSize(50, 20)
        self.pageInput.setAlignment(QtCore.Qt.AlignCenter)
        self.pageInput.setText("1")
        self.pageInput.textChanged.connect(self.handlePageInput)

        self.pageLabel = QtWidgets.QLabel('test')
        bottomHBox.addStretch(1)
        bottomHBox.addWidget(prevButton)
        bottomHBox.addWidget(self.pageInput)
        bottomHBox.addWidget(self.pageLabel)
        bottomHBox.addWidget(nextButton)
        bottomHBox.setSpacing(10)
        bottomHBox.addStretch(1)


        self.addWidget(self.imageLabel)
        self.addLayout(bottomHBox)
    
    def get_numpy_image(self):
        return self.numpy_image
    
    def checkboxStateChanged(self):
        pass
        # self.manager.read_page(self.current_page)
    
    def selectPressed(self):
        self.cvWindow = cv2.namedWindow('Select')
        r = cv2.selectROI("Select", self.numpy_image)
        selected_region = self.numpy_image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        
        self.extract_text_from_image(selected_region)
        cv2.destroyAllWindows()


    def handlePageInput(self, text):
        try:
            page = int(text)
            self.manager.goToPage(page)
            print(f"Entered page: {page}")
        except ValueError:
            print("Invalid page input")


    def prevPressed(self):
        self.manager.goToPage(self.current_page - 1)
    
    def nextPressed(self):
        self.manager.goToPage(self.current_page + 1)

    def setPageCount(self, count):
        self.pageLabel.setText('/ ' + str(count))

    def setImage2Label(self, pix_image, page):
        self.current_page = page
        self.pageInput.setText(str(self.current_page))
        self.numpy_image = self.pix2np(pix_image)
        im = self.numpy2QImage(copy.deepcopy(self.numpy_image))
        
        pixmap = QtGui.QPixmap.fromImage(im)
        self.pix_image_shape = [pixmap.height(), pixmap.width()]
        self.imageLabel.setPixmap(pixmap)
    
    def extract_text_from_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray,lang='tur')
        text = text.replace('\n',' ')
        splitted = text.split('?')
        if len(splitted) > 2:
            new = ''
            for i in range(len(splitted)-1):
                new += splitted[i]
                new += '?'
            question = new
        else:
            question = splitted[0]
        options = self.get_option(splitted[-1])
        self.manager.fill_question_area(question, options)
            
    
    def get_option(self, text):
            subs = ['A)', 'B)', 'C)', 'D)']
            options = []
            try:
                for i in range(len(subs)-1):
                    start_index = text.index(subs[i])
                    end_index = text.index(subs[i+1])
                    options.append(text[start_index:end_index].strip().replace(subs[i],'').strip())
                start_index = text.index('D)')
                options.append(text[start_index:].strip().replace('D)','').strip())
            except:
                options = ['','','','']
            return options
    
    def pix2np(self,pix):
        im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        im = np.ascontiguousarray(im[..., [2, 1, 0]])  # rgb to bgr
        return im
    
    def numpy2QImage(self, npImage):
        npImage = self.image_resize(npImage, width=400)
        height, width, channel = npImage.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(npImage.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)#Format_RGB888
        return qImg

    def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

    
    
