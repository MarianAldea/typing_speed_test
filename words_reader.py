class WordReader():
    def __init__(self):
        self.word_list = []

    def read_words(self):
        with open("words.txt") as file:
            word_bank = file.read().split()
        for word in word_bank:
            self.word_list.append(word)
        return self.word_list