class Mammals:
    def __init__(self):
        self.members = ['Tiger', 'Elephant', 'Wild Cat']


    def printMembers(self):
        print('Printing members of the mammals class...')
        for member in self.members:
            print('\t%s' % member)