class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return(f'Имя: {self.name}\nФамилия:{self.surname}\nСредняя оценка за домашние задания: {self._all_courses_hw_average_grade()}\nЗавершенные курсы: {", ".join(self.finished_courses)}')
 
    def add_course(self, course_name):
        if course_name not in self.courses_in_progress:
            self.courses_in_progress.append(course_name)
        else:
            print("Студент уже проходит этот курс")

    def add_finished_course(self, course_name):
        #Удаление курса из тех, что "в процессе"
        if course_name in self.courses_in_progress:
            self.courses_in_progress.remove(course_name)
        if course_name not in self.finished_courses:
            self.finished_courses.append(course_name)
        else:
            print("Студент уже закончил этот курс")

    def rate_lecturer(self, course_name, rating, lecturer): #выставление студентами оценок преподавателям
        if isinstance(lecturer, Lecturer) and course_name in lecturer.courses_attached and course_name in self.courses_in_progress:
            if (lecturer.courses_rating.get(course_name) == None):
                lecturer.courses_rating[course_name] = [rating]
            else:
                lecturer.courses_rating[course_name].append(rating)
        else:
            print(f'Ошибка - проверьте, правильно ли назначен курс "{course_name}"!')
            return 'Ошибка'
        
    def _all_courses_hw_average_grade(self): #нахождение средней оценки за все выполненные домашние задания
        if self.grades:
            grades_amount = 0
            grades_sum = 0
            for course in self.grades:
                grades_amount += len(self.grades[course])
                grades_sum += sum(self.grades[course])
            return round(grades_sum/grades_amount, 1)
        else:
            #print("Нет ни одной оценки...")
            return 0

    
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

    def __str__(self):
        return(f'Имя: {self.name}\nФамилия:{self.surname}\nСредняя оценка за лекции: {self._all_courses_average_rating()}')

    def _all_courses_average_rating(self): #нахождение средней оценки за все лекции вместе взятые
        if self.courses_rating:
            ratings_amount = 0
            ratings_sum = 0
            for course in self.courses_rating:
                ratings_amount += len(self.courses_rating[course])
                ratings_sum += sum(self.courses_rating[course])
            return round(ratings_sum/ratings_amount, 1)
        else:
            #print("Нет ни одной оценки за лекцию...")
            return 0

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return(f'Имя: {self.name}\nФамилия:{self.surname}')

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
best_student = Student('Ivan', 'Pupkhin', 'prefer_not_say')
#best_student.courses_in_progress += ['Выпечка эчпочмаков', 'ЯП Brainfcuk']
best_student.add_course('Выпечка эчпочмаков')
best_student.add_course('ЯП Brainfcuk')
sanya = Student('Alexander', 'Ivanoff', 'Male')
sanya.courses_in_progress += ['Выпечка эчпочмаков', 'Компьютерные сети и снасти']
#Придумываем ревьюверов, и они ставят студентам оценки
cool_mentor = Reviewer('Мария', 'Аспирантовна-Ревьюер')
cool_mentor.courses_attached += ['Выпечка эчпочмаков', 'ЯП Brainfcuk']
cool_mentor.rate_hw(best_student, 'Выпечка эчпочмаков', 10)
cool_mentor.rate_hw(best_student, 'ЯП Brainfcuk', 10)
cool_mentor.rate_hw(best_student, 'Выпечка эчпочмаков', 9)
#Выставляем оценку студенту по несуществующему курсу
cool_mentor.rate_hw(best_student, 'Компьютерные сети и снасти', 1)
#Добавляем завершенные курсы
best_student.add_finished_course('Исследование НЛО')
sanya.add_finished_course('Продвинутое изучение птиц')

# print(best_student.grades)

#Студент ставит оценку преподавателю курса
some_lecturer = Lecturer('Александр', 'Умнов')
some_lecturer.courses_attached += ['Выпечка эчпочмаков', 'ЯП Brainfcuk']
best_student.rate_lecturer('Выпечка эчпочмаков', 5, some_lecturer)
best_student.rate_lecturer('Выпечка эчпочмаков', 10, some_lecturer)
sanya.rate_lecturer('Выпечка эчпочмаков', 5, some_lecturer)
best_student.rate_lecturer('Компьютерные сети и снасти', 10, some_lecturer)
#Выставляем оценку лектору по несуществующему курсу

# print(some_lecturer.courses_rating)

print(f'РЕВЬЮЕР:\n{cool_mentor}\n----------')
print(f'ЛЕКТОР:\n{some_lecturer}\n----------')
print(f'СТУДЕНТ:\n{sanya}\n----------')
print(f'СТУДЕНТ:\n{best_student}\n----------')