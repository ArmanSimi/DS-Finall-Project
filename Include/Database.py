import Datastructure as Ds
import math
# from typing import Callable


class Admin:
    __user = "آرمان"
    __pass = "412275"

    def __init__(self, username_admin: str = None, password_admin: str = None):
        self.username: str = username_admin
        self.password: str = password_admin
        if username_admin is None:
            self.username = Admin.__user
        if password_admin is None:
            self.password = Admin.__pass

    def login_admin(self, use1: str = None, pass1: str = None):
        if self.username == use1 and self.password == pass1:
            return 1
        elif use1 == "" and pass1 == "":
            return 0
        elif self.username != use1 or self.password != pass1:
            return -1


class Intersections(Ds.DynamicTable, Ds.Trie):
    def __init__(self):
        super(Intersections, self).__init__()
        self.intersections = Ds.DynamicTable()
        self.save_in_trie_intersection = Ds.Trie()

    def __iter__(self):
        return Intersection()

    def show_table_intersection(self):
        for arman in self.intersections.table:
            if isinstance(arman, self.intersections.DNode):
                print(next(arman.value))

    def add_intersection(self, name: str, state: int, st_mode_ns: int = 0, st_mode_ew: int = 1,
                         idx=None, t_ns: int = None, t_ew: int = None, key: int = None):
        new_intersection = Intersection(name, state, st_mode_ns, st_mode_ew, idx, t_ns, t_ew, key)
        self.intersections.insert(new_intersection.key, new_intersection)
        self.save_in_trie_intersection.t_add(name, new_intersection)

    def search_intersection_with_key(self, key: int):
        return self.intersections.find(key)

    def get_intersection_with_key(self, key: int):
        return self.intersections.get_value(key)

    def search_intersection_with_name(self, name: str):
        return self.save_in_trie_intersection.t_find(name)

    def get_intersection_with_name(self, name: str):
        return self.save_in_trie_intersection.t_get(name)

    def delete_intersection(self, name: str, key: int):
        self.intersections.delete(key)
        self.save_in_trie_intersection.t_delete(name)


class Intersection:
    __id = 341075

    def __init__(self, name: str = None, state: int = 0, mode_ns: int = 0, mode_ew: int = 1,
                 idx: int = None, time_ns: int = None, time_ew: int = None, key: int = None):
        self.key = key
        if key is None:
            Intersection.__id += 1
            self.key = Intersection.__id
        if self.key < 99999 or self.key > 999999:
            raise Exception("key error")
        self.name: str = name
        self.state: int = state
        if self.state > 1 or self.state < 0:
            self.state = 0  # Automatic
        if state == 1 or state == 0:
            if mode_ew == "" or mode_ns == "":
                mode_ew = 1
                mode_ns = 0
        self.mode_ew: int = mode_ew
        if mode_ew > 1 or mode_ew < 0:
            self.mode_ew = 0
        self.mode_ns: int = mode_ns
        if mode_ns > 1 or mode_ns < 0:
            self.mode_ns = 0
        if self.mode_ew == 0:
            self.mode_ns = 1
        elif self.mode_ew == 1:
            self.mode_ns = 0
        self.str1 = Street(0, mode_ew)  # شرق غرب
        self.str2 = Street(1, mode_ns)  # شمال جنوب
        self.time_ew: int = time_ew
        if time_ew is None:
            self.time_ew = self.str1.counter
        self.time_ns: int = time_ns
        if time_ns is None:
            self.time_ns = self.str2.counter
        self.count_car = 0
        # self.i = 0
        self.idx = idx
        self.lt = 20
        self.ht = 80
        self.police = None
        # if self.state == 0:
        #     self.automatic_control()
        # if self.state == 1:
        #     self.manual_control(time_ew, time_ns)

        # self.street = [self.str1, self.str2]
        # self.capacity = self.street[0].len + self.street[1].len

    def __iter__(self):
        return self

    def __next__(self):
        return f" چهار راهی به اسم {self.name} و کد {self.key} موجود می باشد "

    def manual_control(self):
        self.str1.counter = self.time_ew
        self.str2.counter = self.time_ns
        if self.str1.color == 1:
            self.mode_ew = self.str1.color = 0
            self.mode_ns = self.str2.color = 1
        elif self.str1.color == 0:
            self.mode_ew = self.str1.color = 1
            self.mode_ns = self.str2.color = 0

    def automatic_control(self):
        # red = 1, green = 0
        # str1 = 0 : شرق غرب, str2 = 1 : شمال جنوب
        if self.str1.color == 1:
            self.mode_ew = self.str1.color = 0
            self.mode_ns = self.str2.color = 1
            if self.count_car == self.str1.counter * 2:
                self.str1.counter += math.floor((3 / 5 * self.str1.counter))
                if self.str1.counter > self.ht:
                    self.str1.counter = self.ht
                self.time_ew = self.str1.counter
            elif self.count_car < self.str1.counter * 2:
                self.str1.counter -= math.floor((2 / 5 * self.str1.counter))
                if self.str1.counter < self.lt:
                    self.str1.counter = self.lt
                self.time_ew = self.str1.counter
        elif self.str1.color == 0:
            self.mode_ew = self.str1.color = 1
            self.mode_ns = self.str2.color = 0
            if self.count_car == 2 * self.str2.counter:
                self.str2.counter += math.floor((3 / 5 * self.str2.counter))
                if self.str2.counter > self.ht:
                    self.str2.counter = self.ht
                self.time_ns = self.str2.counter
            elif self.count_car < self.str2.counter * 2:
                self.str2.counter -= math.floor((2 / 5 * self.str2.counter))
                if self.str2.counter < self.lt:
                    self.str2.counter = self.lt
                self.time_ns = self.str2.counter

    def get_amount_car(self):
        return self.count_car

    def get_counter_ew(self):
        return self.str1.counter

    def get_counter_ns(self):
        return self.str2.counter


class Street:  # (Ds.Sll)
    def __init__(self, name: int = 0, color: int = 0, counter: int = 20):
        # super(Street, self).__init__()
        self.name = name
        if self.name > 1 or self.name < 0:
            self.name = 0
        self.color = color
        self.counter = counter
        if self.name == 0:
            self.name = "EW"
        if self.name == 1:
            self.name = "NS"
        # self.cars = Ds.Sll()
        # self.inverse_cars = Ds.Sll()
        # self.len = self.cars.get_len() + self.inverse_cars.get_len()


class Polices(Ds.DynamicTable, Ds.Trie):
    def __init__(self):
        super(Polices, self).__init__()
        self.polices = Ds.DynamicTable()
        self.save_in_trie_police = Ds.Trie()

    def add_police(self, name: str, national_code: int, register_time: str, salary: str, idx: int):
        new_police = Police(name, national_code, register_time, salary, idx)
        self.polices.insert(new_police.national_code, new_police)
        self.save_in_trie_police.t_add(name, new_police)

    def search_police_with_key(self, key: int):
        return self.polices.find(key)

    def get_police_with_key(self, key: int):
        return self.polices.get_value(key)

    def search_police_with_name(self, name: str):
        return self.save_in_trie_police.t_find(name)

    def get_police_with_name(self, name: str):
        return self.save_in_trie_police.t_get(name)


class Police(Ds.Sll, Ds.Queue):
    def __init__(self, name: str, national_code: int, register_time: str, salary: str, idx: int = None):
        super(Police, self).__init__()
        self.name: str = name
        self.national_code: int = national_code
        self.registerTime: str = register_time
        self.salary: str = salary
        self.absence = 0
        self.attendance = 0
        self.state = 0  # 0 = غایب , 1 = حاضر
        # self.sms = sms_callable
        # self.clock_func = clock_func
        if self.national_code < 1000000000 or self.national_code > 9999999999:
            raise Exception("national code error: the code entered out of range")
        self.payedSalary = Ds.Sll()
        self.shift = Ds.Queue(5)
        self.idx = idx

    def __iter__(self):
        return self, PayedSalary(self), ShiftPolice(self)

    def __next__(self):
        return f" پلیس به اسم {self.name} و کد ملی {self.national_code} از تاریخ {self.registerTime}" \
               f" در سیستم ثبت شده است "

    def first_location(self):
        return self.shift.show_first()

    def next_location(self):
        return self.shift.show_next_first()

    def add_shift(self, time_shift: int, key_intersection: int):
        result_check_time = self.check_duplicate_new(time_shift)
        if not result_check_time:
            new_shift = ShiftPolice(self, time_shift, key_intersection)
            if (self.shift.size() + 1) == len(self.shift.queue):
                return False, -1
            else:
                self.shift.enqueue(new_shift)
                return True, new_shift
        else:
            return False, -2

    def del_shift(self):
        return self.shift.dequeue()

    def display_shift(self):
        for shift in range(len(self.shift.queue)):
            if isinstance(self.shift.queue[shift], ShiftPolice):
                print(next(self.shift.queue[shift]))

    def check_duplicate_new(self, time_shift):
        for shift in range(len(self.shift.queue)):
            if isinstance(self.shift.queue[shift], ShiftPolice):
                if self.shift.queue[shift].time_shift == time_shift:
                    return True
            else:
                continue
        return False

    def check_duplicate_time_shift(self):
        flag = False
        for shift in range(len(self.shift.queue)):
            if isinstance(self.shift.queue[shift], ShiftPolice):
                index = (shift + 1) % len(self.shift.queue)
                for next_shift in range(index, len(self.shift.queue)):
                    print(next_shift)
                    if isinstance(self.shift.queue[next_shift], ShiftPolice):
                        if self.shift.queue[shift].time_shift == self.shift.queue[next_shift].time_shift:
                            flag = True
                            return flag
                        elif index == (len(self.shift.queue) - 1):
                            return flag
                    else:
                        continue
            else:
                continue
        return flag

    def payed_salary(self, time_payed_salary: str = None, amount_payed_salary: int = None):
        salary = PayedSalary(self, time_payed_salary, amount_payed_salary)
        self.payedSalary.insert_last(salary)

    def display_salary(self):
        simi = self.payedSalary.traverse()
        for arman in simi:
            print(next(arman))


class ShiftPolice:
    def __init__(self, police: Police, time_shift: int = None, key_intersection_shift: int = None):
        self.police = police
        self.time_shift: int = time_shift
        while time_shift >= 24:
            time_shift = time_shift - 24
            self.time_shift = time_shift
        self.next_time_shift = self.time_shift + 1
        self.intersection_shift: int = key_intersection_shift
        self.clock_time = (((self.time_shift - 1) * 60) + 50) * 60
        self.i_shift = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i_shift == 0:
            self.i_shift += 1
            return f"اسم: {self.police.name} کد ملی: {self.police.national_code}" \
                   f" زمان شیفت: {self.next_time_shift} - {self.time_shift}  مکان: {self.intersection_shift}"
        else:
            raise StopIteration


class PayedSalary:
    __count_salary = 0
    __time_payed_salary = 30
    __amount_salary = 45000

    def __init__(self, police: Police, time_payed_salary: str = None, amount: int = None, info: str = None):
        self.police = police
        self.info: str = info
        self.timePayedSalary: str = time_payed_salary
        self.amount: int = amount

        if amount is None:
            self.amount = PayedSalary.__amount_salary

        if time_payed_salary is None:
            self.timePayedSalary = PayedSalary.__time_payed_salary

        if info is None:
            PayedSalary.__count_salary += 1
            self.info = f" حقوق شماره {PayedSalary.__count_salary} برای مدت {self.timePayedSalary}" \
                        f" روز به میزان {self.amount} پرداخت شد "
        self.i_salary = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i_salary == 1:
            self.i_salary += 1
            return self.info
        elif self.i_salary == 0:
            self.i_salary += 1
            return f"name: {self.police.name}, national code: {self.police.national_code}, salary: " \
                   f"{self.police.salary}, register time: {self.police.registerTime}, payroll: {self.info}"
        else:
            raise StopIteration
