import fitz
from PySide6 import QtCore, QtWidgets, QtGui
from widgets.leftLayout import LeftLayout
from widgets.rightLayout import RightLayout
from dataType import QuestionData
import cv2
import re

class ManagerScreen(QtWidgets.QWidget):
    def __init__(self, firebase, file_path, exam_ref, exam_type, exam_name, answer_page):
        super().__init__()

        self.firebase = firebase

        self.exam_ref = exam_ref
        self.exam_type = exam_type
        self.exam_name = exam_name
        self.question_array = []
        self.answerKey_page = int(answer_page)
        self.answers = {}

        self.setWindowTitle("Yeni Pencere")
        
        layout = QtWidgets.QVBoxLayout(self)
        splitter = QtWidgets.QSplitter()
        splitter.setChildrenCollapsible(False)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        # left widget
        leftSide= QtWidgets.QWidget()
        self.leftVBox = LeftLayout(self, exam_name, exam_type)
        leftSide.setLayout(self.leftVBox)

        # right widget
        rightSide= QtWidgets.QWidget()
        self.rightVBox = RightLayout(self)#QtWidgets.QVBoxLayout()
        rightSide.setLayout(self.rightVBox)

        splitter.addWidget(leftSide)
        splitter.addWidget(rightSide)

        layout.addWidget(splitter)

        self.open_pdf(file_path)
    
    def get_numpy_image(self):
        return self.rightVBox.get_numpy_image()

    def get_answers(self):
        return self.answers
    
    def append_array(self,q_num,quest,q_image,options,opt_image,ans,desc):
        question = QuestionData(q_num,quest,q_image,options,opt_image,ans,desc)
        self.question_array.append(question)
    
    def sendFirebase(self):
        print(self.exam_ref,self.exam_name)
        self.firebase.send2firebase(self.exam_ref,self.exam_name, self.question_array)
    
    def open_pdf(self, path):
        self.doc = fitz.open(path)
        self.rightVBox.setPageCount(self.doc.page_count)
        self.answers = self.read_answer_key()
        self.leftVBox.init_first_question()
        self.goToPage(1)
    
    def fill_question_area(self, question, options):
        self.leftVBox.fill_question_area(question, options)


    def read_answer_key(self):
        answerPage = self.doc.load_page(self.answerKey_page-1)
        text = answerPage.get_text()
        data = text.split('\n')
        answer_key_start = -1
        answer_key = {}
        for i, item in enumerate(data):
            if item.startswith('1.'):
                if i < len(data) - 1 and data[i + 1].startswith('2.'):
                    answer_key_start = i
                break

        if answer_key_start != -1:
            answer_key_section = data[answer_key_start:]
        else:
            return None
        
        for item in answer_key_section:
            parts = item.split('.')
            if len(parts) == 2:
                question_number = parts[0].strip()
                answer = parts[1].strip()
                answer_key[question_number] = answer
        # print(answer_key)
        return answer_key

    
    def goToPage(self, pageNum):
        if pageNum > 0 and pageNum <= self.doc.page_count:
            pass
        else:
            pageNum = 1
        page = self.doc.load_page(pageNum-1)
        # pix_map = page.get_pixmap()
        zoom_x = 2.0  # horizontal zoom
        zoom_y = 2.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y) 
        pix_map = page.get_pixmap(matrix=mat)
        self.rightVBox.setImage2Label(pix_map, pageNum)
    

    # TODO: improve this feature
    def question_parser(self, text):
        text = text.replace('\n','')
        pattern = r'(\d+\.)(.+?)([A-D]\))(.*?)((?=\d+\.)|$)'
        matches = re.findall(pattern, text, re.DOTALL)
        print(matches)
        question_num = int(re.search(r'\d+', text).group())
        question_content = re.search(r'\d+\.\s(.+)', text).group(1)
        choices = re.findall(r'[A-D]\)\s(.+)', text)
        # print(re.findall(r'\d+', text))
        # print(question_num)
        # print(question_content)
        # print(choices)

    def read_page(self, page_num):
        page = self.doc.load_page(page_num-1)

        page_width = page.rect.width
        page_height = page.rect.height

        # Header ve footer yüksekliği
        header_height = 70
        footer_height = 70

        # Rect koordinatlarını belirle
        x1 = 0
        y1 = header_height
        x2 = page_width
        y2 = page_height - footer_height

        # Sayfa orta noktasını hesapla
        mid_point = page_width / 2

        # Sol taraftaki metinlerin dikdörtgeni
        left_rect = fitz.Rect(0, header_height, mid_point-10, page_height - footer_height)
        left_text = page.get_textbox(left_rect)
        print("Sol Taraftaki Metinler:")
        self.question_parser(left_text)
        print("\n\n\n\n\n")

        # Sağ taraftaki metinlerin dikdörtgeni
        right_rect = fitz.Rect(mid_point+10, header_height, page_width, page_height - footer_height)
        right_textbox = page.get_textbox(right_rect)
        print("Sağ Taraftaki Metinler:")
        print(right_textbox)

        # # Dikdörtgeni oluştur
        # rect = fitz.Rect(x1, y1, x2, y2)
        # textbox = page.get_textbox(rect)
        # print(textbox)