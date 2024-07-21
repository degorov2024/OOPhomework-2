class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
 
    def add_courses(self, course_name):
        self.finished_courses.append(course_name)   

    def rate_lecturer(self, course_name, rating, lecturer): #выставление студентами оценок преподавателям
        if isinstance(lecturer, Lecturer) and course_name in lecturer.courses_attached and course_name in self.courses_in_progress:
            lecturer.courses_rating[course_name] = [rating] if (lecturer.courses_rating.get(course_name) == None) else lecturer.courses_rating[course_name].append(rating)
        else:
            print(f'Ошибка - проверьте, правильно ли назначен курс "{course_name}" !')
            return 'Ошибка'

    
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.name = name
        self.surname = surname
        self.courses_rating = {} # словарь типа {'Курс по выпечке эчпочмаков':[10, 9, 2, 1, 10], 'Менеджмент':[3, 2, 9]}
        self.courses_attached = []

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade): #выставление студентам оценки за дз
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print(f'Ошибка - проверьте, правильно ли назначен курс "{course}" !')
            return 'Ошибка'

#Придумываем студентов и назначаем им курсы
best_student = Student('Ivan', 'Poopkhin', 'prefer_not_say')
best_student.courses_in_progress += ['Выпечка эчпочмаков', 'ЯП Brainfcuk']
#Придумываем ревьюверов, и они ставят студентам оценки
cool_mentor = Reviewer('Мария', 'Аспирантовна-Ревьюер')
cool_mentor.courses_attached += ['Выпечка эчпочмаков', 'ЯП Brainfcuk']
cool_mentor.rate_hw(best_student, 'Выпечка эчпочмаков', 10)
cool_mentor.rate_hw(best_student, 'ЯП Brainfcuk', 10)
cool_mentor.rate_hw(best_student, 'Выпечка эчпочмаков', 9)
#Выставляем оценку студенту по несуществующему курсу
cool_mentor.rate_hw(best_student, 'Компьютерные сети и снасти', 1)

print(best_student.grades)

#Студент ставит оценку преподавателю курса
some_lecturer = Lecturer('Александр', 'Умнов')
some_lecturer.courses_attached += ['Выпечка эчпочмаков', 'ЯП Brainfcuk']
best_student.rate_lecturer('Выпечка эчпочмаков', 5, some_lecturer)
best_student.rate_lecturer('Компьютерные сети и снасти', 10, some_lecturer)
#Выставляем оценку лектору по несуществующему курсу
print(some_lecturer.courses_rating)