class Fish:
    def __init__(self):
        self.members = ['Salmon', 'Sill', 'Pike']


    def printMembers(self):
        print('Printing members of the fish class...')
        for member in self.members:
            print('\t%s' % member)