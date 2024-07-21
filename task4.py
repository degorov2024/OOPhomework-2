class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return(f'Имя: {self.name}\nФамилия:{self.surname}\nСредняя оценка за '
               f'домашние задания: {self._all_courses_hw_average_grade()}\n'
               f'Завершенные курсы: {", ".join(self.finished_courses)}')
 
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

    #выставление студентами оценок преподавателям
    def rate_lecturer(self, course_name, rating, lecturer):
        if (isinstance(lecturer, Lecturer) and course_name 
            in lecturer.courses_attached and course_name 
            in self.courses_in_progress):
            if (lecturer.courses_rating.get(course_name) == None):
                lecturer.courses_rating[course_name] = [rating]
            else:
                lecturer.courses_rating[course_name].append(rating)
        else:
            print(f'Ошибка - проверьте, правильно ли назначен '
                  f'курс "{course_name}"!')
            return 'Ошибка'

    #нахождение средней оценки за все выполненные домашние задания    
    def _all_courses_hw_average_grade(self):
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

    #нахождение средней оценки за выполненные д/з по ОДНОМУ курсу    
    def course_hw_average_grade(self, course):
        if self.grades[course]:
            grades_amount = len(self.grades[course])
            grades_sum = sum(self.grades[course])
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
        # словарь типа {'Курс по выпечке эчпочмаков':[10, 9, 2, 1, 10],..
        self.courses_rating = {}
        self.courses_attached = []

    def __str__(self):
        return(f'Имя: {self.name}\nФамилия:{self.surname}\nСредняя оценка за '
               f'лекции: {self._all_courses_average_rating()}')

    #нахождение средней оценки за все лекции вместе взятые
    def _all_courses_average_rating(self):
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

    #нахождение средней оценки за ОДИН КУРС    
    def course_average_rating(self, course):
        if self.courses_rating[course]:
            ratings_amount = 0
            ratings_sum = 0
            ratings_amount = len(self.courses_rating[course])
            ratings_sum = sum(self.courses_rating[course])
            return round(ratings_sum/ratings_amount, 1)
        else:
            #print("Нет ни одной оценки за лекцию...")
            return 0
        
    #Методы сравнения по средней оценке - в лекции было сказано, 
    # что можно реализовать только == и <
    def __lt__(self, other):
        if (self._all_courses_average_rating() < 
            other._all_courses_average_rating()):
            return True
        else:
            return False

    def __eq__(self, other):
        if (self._all_courses_average_rating() == 
            other._all_courses_average_rating()):
            return True
        else:
            return False   


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return(f'Имя: {self.name}\nФамилия:{self.surname}')

    #выставление студентам оценки за дз
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and course in self.courses_attached 
            and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print(f'Ошибка - проверьте, правильно ли назначен '
                  f'курс "{course}" !')
            return 'Ошибка'


#Подсчет средней оценки за д/з по всем студентам в рамках конкретного курса
def average_course_students_grade(students, course):
    grades_sum = 0
    students_num = 0
    for student in students:
        if course in student.grades:
            grades_sum += student.course_hw_average_grade(course)
            students_num += 1
    if students_num == 0:
        return 0 
    else:
        return round(grades_sum/students_num, 1)

def average_course_lecturers_grade(lecturers, course):
    rating_sum = 0
    lecturers_num = 0
    for lecturer in lecturers:
        if course in lecturer.courses_rating:
            rating_sum += lecturer.course_average_rating(course)
            lecturers_num += 1
    if lecturers_num == 0:
        return 0 
    else:
        return round(rating_sum/lecturers_num, 1)


#Эти менторы ничего не умеют делать, т.к. они просто примеры экземпляров
#родительского класса
mentor1 = Mentor('Мария', 'Иванова')
mentor1.courses_attached = ["Бизнес-мышление"]
mentor2 = Mentor('Борис', 'Бобров')
mentor1.courses_attached = ["Выпечка эчпочмаков", "Прыжки с парашютом "
                            f"на северном полюсе"]

#Придумываем студентов и назначаем им курсы
best_student = Student('Ivan', 'Pupkhin', 'prefer_not_say')
best_student.add_course('Выпечка эчпочмаков')
best_student.add_course('ЯП Brainfcuk')
sanya = Student('Alexander', 'Ivanoff', 'Male')
sanya.add_course('Выпечка эчпочмаков')
sanya.add_course('Компьютерные сети и снасти')
#Придумываем ревьюверов, и они ставят студентам оценки
cool_mentor = Reviewer('Мария', 'Аспирантовна-Ревьюер')
cool_mentor.courses_attached += ['Выпечка эчпочмаков', 'ЯП Brainfcuk']
cool_mentor_2 = Reviewer('Сергей', 'Проверяющий')
cool_mentor_2.courses_attached += ['Выпечка эчпочмаков']
cool_mentor.rate_hw(best_student, 'Выпечка эчпочмаков', 10)
cool_mentor.rate_hw(best_student, 'ЯП Brainfcuk', 10)
cool_mentor_2.rate_hw(best_student, 'Выпечка эчпочмаков', 9)
cool_mentor_2.rate_hw(sanya, 'Выпечка эчпочмаков', 2)
cool_mentor_2.courses_attached += ['Компьютерные сети и снасти']
cool_mentor_2.rate_hw(sanya, 'Компьютерные сети и снасти', 8)
#Выставляем оценку студенту по неназначенному курсу
cool_mentor.rate_hw(best_student, 'Компьютерные сети и снасти', 1)
#Добавляем завершенные курсы
best_student.add_finished_course('Исследование НЛО')
sanya.add_finished_course('Продвинутое изучение птиц')

#Студент ставит оценку преподавателю курса
some_lecturer = Lecturer('Александр', 'Умнов')
some_lecturer.courses_attached += ['Выпечка эчпочмаков', 'ЯП Brainfcuk']
best_student.rate_lecturer('Выпечка эчпочмаков', 5, some_lecturer)
best_student.rate_lecturer('Выпечка эчпочмаков', 10, some_lecturer)
sanya.rate_lecturer('Выпечка эчпочмаков', 5, some_lecturer)
#Выставляем оценку лектору по неназначенному курсу
best_student.rate_lecturer('Компьютерные сети и снасти', 10, some_lecturer)
some_lecturer_2 = Lecturer('Константин', 'Златоустов')
some_lecturer_2.courses_attached += ['Выпечка эчпочмаков', 'Компьютерные '
                                     f'сети и снасти']
sanya.rate_lecturer('Компьютерные сети и снасти', 7, some_lecturer_2)
sanya.rate_lecturer('Выпечка эчпочмаков', 2, some_lecturer_2)

print(f'\nРЕВЬЮЕР:\n{cool_mentor}\n----------')
print(f'ЛЕКТОР:\n{some_lecturer}\n----------')
print(f'ЛЕКТОР:\n{some_lecturer_2}\n----------')
print(f'СТУДЕНТ:\n{sanya}\n----------')
print(f'СТУДЕНТ:\n{best_student}\n----------')

print("Сравнение лекторов:")
if some_lecturer == some_lecturer_2:
    print('Средние оценки одинаковые!')
else:
    print('Есть разница в средней оценке...')
    if some_lecturer_2 < some_lecturer:
        print(f'Оценка больше у лектора {some_lecturer.name} '
              f'{some_lecturer.surname}') 
    else:
        (print(f'Оценка больше у лектора {some_lecturer_2.name} '
               f'{some_lecturer_2.surname}'))

print("\nСредняя оценка студентов за выпечку эчпочмаков:")
print(average_course_students_grade([sanya, best_student], 
                                    'Выпечка эчпочмаков'))
print("Средняя оценка лекторов за ведение выпечки эчпочмаков:")
print(average_course_lecturers_grade([some_lecturer, some_lecturer_2], 
                                     'Выпечка эчпочмаков'))