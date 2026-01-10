class CharacterCounterClass:
    def __init__(self):
        self.fd = None

    def open_file(self):
        self.fd = open('a1q1b/lorem-ipsum.txt')

    def close_file(self):
        self.fd.close()

    def get_content(self):
        return self.fd.read()

    def count_characters(self):
        content = self.get_content()
        counter = 0
        for line in content:
            counter += len(line)
        return counter

if __name__ == "__main__":
    cc = CharacterCounterClass()
    cc.open_file()
    print(cc.count_characters())
    cc.close_file()
    
