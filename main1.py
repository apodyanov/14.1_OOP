
class Employee:
    name: str
    surname: str
    email: str
    pay: int

    def __init__(self, name, surname, pay):
        self.name = name
        self.surname = surname
        self.pay = pay
        self.email = f'{self.name}.{self.surname}@gmail.com'
        self.is_work = False
        self.is_vacation = False

    def work(self):
        self.is_work = True
        print('Do some work')

    def go_to_vacation(self):
        self.is_vacation = True
        print('Go to vacation')

if __name__=='__main__':
    emp_1 = Employee('Ivan', 'Ivanov', 50_000)

    print(emp_1)
    print(emp_1.name)
    print(emp_1.surname)
    print(emp_1.email)
    print(emp_1.pay)


# emp_1 = Employee('Ivan', 'Ivanov', 50_000)
#
# print(emp_1.name)
# print(emp_1.surname)
# print(emp_1.email)
# print(emp_1.pay)


# Это создание атрибутов объекта в ручную
# emp_1 = Employee()
# emp_2 = Employee()
#
# emp_1.name = 'Ivan'
# emp_1.surname = 'Ivanov'
# emp_1.email = 'Ivanov@mail.ru'
# emp_1.pay = 50_000
#
# emp_2.name = 'Petr'
# emp_2.surname = 'Petrov'
# emp_2.email = 'Penrov@mail.ru'
# emp_2.pay = 60_000
#
#
# print(emp_2.name)
# print(emp_1.name)