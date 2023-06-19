class QuestionData:
    def __init__(self, number, question, q_image_url, options, opt_image_url, answer, description):
        super().__init__()

        self.number = number
        self.question = question
        self.options = options
        self.opt_image_url = opt_image_url
        self.answer = answer
        self.q_image_url = q_image_url
        self. description = description 