class Person:
    def __init__(self, firstName: str, lastName: str):
        self.firstName = firstName
        self.lastName = lastName

    def getFullName(self):
        fullName = self.firstName + " " + self.lastName
        return fullName
    

class Student(Person):
    def __init__(self, firstName: str, lastName: str, subject: str):
        super().__init__(firstName, lastName)
        self.subject = subject

    def getStudentDetails(self):
        nameSubject = self.getFullName() + " takes " + self.subject
        print(nameSubject)


class Teacher(Person):
    def __init__(self, firstName: str, lastName: str, course: str):
        super().__init__(firstName, lastName)
        self.course = course

    def getTeacherDetails(self):
        nameCourse = self.getFullName() + " teaches " + self.course
        print(nameCourse)