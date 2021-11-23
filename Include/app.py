import Database as Adt
import tkinter as tk
from tkinter import messagebox
from typing import Callable
from threading import Thread
from time import perf_counter, process_time
import pickle

start_perfCounter = perf_counter()
start_processTime = process_time()


with open('arman.simi', 'rb') as file:
    result_file = pickle.load(file)


# page
app = None
home = None
cross = None
police = None
# event after
app_after = None
home_after = None
cross_after = None
police_after = None
# time
date = None
date_home = None
date_polices = None
date_intersection = None
counter = 0
help_counter = 0
second = 0
minute = 0
hour = 0
day = 0
time = ""
# login page
e_user = None
e_pass = None

"""
global amounts table intersection
"""
cell_i = None
idx_i = 3
name_intersection_city = ""
state_intersection = ""
mode_ns = ""
mode_ew = ""
time_ns = ""
time_ew = ""

entry_search_name_cross = None
entry_search_key_cross = None
lb_result_search_intersection = ""

"""
global amounts table police
"""
cell_p = None
idx_p = 3
name_police = ""
ntc_police = ""

en_search_address = None
en_search_code = None
en_search_name = None
lb_result_search_police = ""
# police
en_shift = None
en_key_shift = None
en_code_intersection = None
shift_box = None
# callable
c_light = None
c_sms = None


class ControlPanel(Adt.Admin, Adt.Intersections, Adt.Polices):
    def __init__(self):
        super(ControlPanel, self).__init__()
        self.admin = Adt.Admin("آرمان", "1")
        self.control_intersections = Adt.Intersections()
        self.control_polices = Adt.Polices()

    def login(self, user1, pass1):
        return self.admin.login_admin(user1, pass1)
    """
    Add Intersection and search with key or name
    """
    def cp_add_intersection(self, name: str, state: int, st_mod_ns: int = 0, st_mod_ew: int = 1, idx=None,
                            tim_ns: int = None, tim_ew: int = None, key: int = None):
        self.control_intersections.add_intersection(name, state, st_mod_ns, st_mod_ew, idx, tim_ns, tim_ew, key)

    def cp_search_intersection_with_key(self, key: int):
        return self.control_intersections.search_intersection_with_key(key)

    def cp_get_intersection_with_key(self, key: int):
        return self.control_intersections.get_intersection_with_key(key)

    def cp_search_intersection_with_name(self, name: str):
        return self.control_intersections.search_intersection_with_name(name)

    def cp_get_intersection_with_name(self, name: str):
        return self.control_intersections.get_intersection_with_name(name)

    def cp_delete_intersection(self, name: str, key: int):
        self.control_intersections.delete_intersection(name, key)
    """
    Add Police and search with key or name or location
    """
    def cp_add_police(self, name: str, ntc: int, register_time: str, salary: str, idx):
        self.control_polices.add_police(name, ntc, register_time, salary, idx)

    def cp_get_police_with_key(self, ntc: int):
        return self.control_polices.get_police_with_key(ntc)

    def cp_get_police_with_name(self, name: str):
        return self.control_polices.get_police_with_name(name)


CP = ControlPanel()


def init(light: Callable, sms: Callable):
    global c_light, c_sms
    c_light = light
    c_sms = sms
    login()


def attendance(intersection_id, agent_id):
    intersection = CP.cp_get_police_with_key(int(intersection_id))
    res_police = CP.cp_get_police_with_key(agent_id)
    intersection.police = res_police.name
    res_police.state = 1
    res_police.attendance += 1


def clock():
    global counter, second, minute, hour, day, time, help_counter
    counter += 1
    second += 1
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour += 1
    if hour == 24:
        hour = 0
        day += 1
        help_counter = 1
    if help_counter == 1:
        counter = 0
        help_counter = 0
    time = f"روز {day} ساعت {second} : {minute} : {hour}"
    update_table_intersection()
    update_table_police()
    clear_shift_box()


def login():
    global e_user, e_pass, date, app  # app_after
    app = tk.Tk()
    app.geometry("540x410")
    app.minsize(540, 410)
    app.maxsize(540, 410)
    app.title("پنل ورود")
    header_text = tk.Label(app, text="نرم افزار راهنمایی رانندگی شهر اهواز", fg="green")
    header_text.pack(pady=30)
    date = tk.Label(app, text="", fg="darkblue")
    date.pack(pady=14)
    username_lb = tk.Label(app, text="نام کاربری خود را وارد کنید", fg="green")
    username_lb.pack(pady=7)
    e_user = tk.Entry(app, width=22)
    e_user.pack(pady=7)
    password_lb = tk.Label(app, text="رمز عبور خود را وارد کنید", fg="green")
    password_lb.pack(pady=7)
    e_pass = tk.Entry(app, width=22)
    e_pass.pack(pady=7)
    btn_log = tk.Button(app, text="ورود به صحفه اصلی", command=btn_login, bg="green", fg="white")
    btn_log.pack(pady=7, ipadx=14, ipady=1)
    clock_updater_login()
    app.mainloop()
    app.after_cancel(app_after)


def btn_login():
    # global e_user, e_pass
    username = e_user.get()
    password = e_pass.get()
    result_login = ControlPanel().login(username, password)
    if result_login == 1:
        home_page(username)
    elif result_login == 0:
        messagebox.showwarning("!هشدار خالی بودن فرم", "نام کاربری و رمز خود را وارد کنید")
    else:
        messagebox.showerror("خطای ورودی اشتباه", "نام کاربری و رمز عبور اشتباه می باشد")


def home_page(username):
    global date_home, home, app  # home_after
    home = tk.Tk()
    app.destroy()
    home.geometry("540x410")
    home.minsize(540, 410)
    home.maxsize(540, 100)
    home.title("صحفه اصلی")
    menubar = tk.Menu(home)
    menubar.add_command(label="چهار راه ها", command=intersection_page)
    menubar.add_command(label="ماموران راهنمایی رانندگی", command=traffic_polices_page)
    menubar.add_command(label="خروج", command=home.quit)
    home.config(menu=menubar)
    header_text_home_page = tk.Label(home, text="نرم افزار راهنمایی رانندگی شهر اهواز", fg="green")
    header_text_home_page.pack(pady=30)
    date_home = tk.Label(home, text="", fg="darkblue")
    date_home.pack(pady=25)
    home_label = tk.Label(home, text=f"سلام {username} می تونی با استفاده از\n منو به صحفه کنترل چهار راه ها و \n"
                                     f" مامورین راهنمایی رانندگی دسترسی داشته باشی", fg="green")
    home_label.pack(pady=10)
    clock_updater_home()
    home.mainloop()
    home.after_cancel(home_after)


def intersection_page():
    global date_intersection, cross, lb_result_search_intersection, cell_i,\
        entry_search_name_cross, entry_search_key_cross  # cross_after
    cross = tk.Toplevel(home)
    cross.geometry("850x500")
    cross.minsize(850, 500)
    cross.maxsize(850, 500)
    cross.title("پنل کنترل چهار راه ها و چراغ های راهنمایی رانندگی")
    menu_intersection = tk.Menu(cross)
    menu_intersection.add_command(label="ماموران راهنمایی رانندگی", command=traffic_polices_page)
    menu_intersection.add_command(label="خروج", command=cross.quit)
    cross.config(menu=menu_intersection)
    date_intersection = tk.Label(cross, text="", fg="darkblue")
    date_intersection.grid(row=0, columnspan=8, pady=10)
    lb_search_name_cross = tk.Label(cross, text=" سرچ با استفاده \nاز نام چهار راه ", fg="darkgreen")
    lb_search_name_cross.grid(row=1, columnspan=4, pady=4)
    entry_search_name_cross = tk.Entry(cross, width=17)
    entry_search_name_cross.grid(row=1, column=1, columnspan=4)
    lb_search_key_cross = tk.Label(cross, text=" سرچ با استفاده\nاز کد چهار راه ", fg="darkgreen")
    lb_search_key_cross.grid(row=1, column=1, columnspan=6)
    entry_search_key_cross = tk.Entry(cross, width=17)
    entry_search_key_cross.grid(row=1, column=3, columnspan=4)
    btn_submit_search_intersection = tk.Button(cross, text="جستجو", fg="darkgreen", bd=0, command=search_intersection)
    btn_submit_search_intersection.grid(row=1, column=4, columnspan=5)
    lb_result_search_intersection = tk.Label(cross, text="پنل کنترل چهار راه ها و چراغ های راهنمایی رانندگی شهر اهواز",
                                             fg="darkgreen")
    lb_result_search_intersection.grid(row=2, columnspan=8, pady=6)

    width = 8
    height = 23
    cell_i = {}
    for i in range(width):
        for j in range(3, height):
            b = tk.Entry(cross, width=17)
            b.grid(row=j, column=i)
            cell_i[(j, i)] = b

    cell_i[(3, 0)].insert(0, "شمارشگر شرق-غرب")
    cell_i[(3, 1)].insert(0, "وضعیت شرق-غرب")
    cell_i[(3, 2)].insert(0, "شمارشگرشمال-جنوب")
    cell_i[(3, 3)].insert(0, "وٍضعیت شمال جنوب")
    cell_i[(3, 4)].insert(0, "تعدادماشینهای عبوری")
    cell_i[(3, 5)].insert(0, "حالت اتوماتیک/دستی")
    cell_i[(3, 6)].insert(0, "کد 6 رقمی چهار راه")
    cell_i[(3, 7)].insert(0, "اسم چهار راه شهر")

    for i in range(width):
        cell_i[(3, i)].config(state='disable')

    # for i in range(3, height):
    #     cell_i[(i, 4)].config(state='disable')
    # for i in range(3, height):
    #     cell_i[(i, 6)].config(state='disable')

    for j in range(3, height):
        cell_i[(j, 0)].bind('<KeyPress>', field_time_ew)
    for j in range(3, height):
        cell_i[(j, 1)].bind('<KeyPress>', field_mode_ew)
    for j in range(3, height):
        cell_i[(j, 2)].bind('<KeyPress>', field_time_ns)
    for j in range(3, height):
        cell_i[(j, 3)].bind('<KeyPress>', field_mode_ns)
    for j in range(3, height):
        cell_i[(j, 5)].bind('<KeyPress>', field_state_intersection)
    for j in range(3, height):
        cell_i[(j, 7)].bind('<KeyPress>', field_name_intersection)

    cross.bind('<KeyPress>', send_information_intersection)
    clock_updater_intersection()
    cross.mainloop()
    cross.after_cancel(cross_after)


def traffic_polices_page():
    global police, date_polices, cell_p, lb_result_search_police, en_search_address, en_search_code,\
        en_search_name, en_key_shift, en_shift, en_code_intersection, shift_box  # police_after
    police = tk.Toplevel(home)
    police.geometry("950x720")
    police.minsize(950, 720)
    police.maxsize(950, 720)
    police.title("پنل ماموران راهنمایی رانندگی")
    menu_police = tk.Menu(police)
    menu_police.add_command(label="چهار راه ها", command=intersection_page)
    menu_police.add_command(label="خروج", command=police.quit)
    police.config(menu=menu_police)
    date_polices = tk.Label(police, text="", fg="darkblue")
    date_polices.grid(row=0, pady=7, columnspan=7)
    lb_search_name = tk.Label(police, text="جستجو با اسم مامور\nراهنمایی رانندگی", fg="darkgreen")
    lb_search_name.grid(row=1, column=0, pady=8, columnspan=2)
    en_search_name = tk.Entry(police, width=21)
    en_search_name.grid(row=1, column=1, columnspan=2)
    lb_search_code = tk.Label(police, text="جستجو با کدملی مامور\nراهنمایی رانندگی", fg="darkgreen")
    lb_search_code.grid(row=1, column=2, columnspan=2)
    en_search_code = tk.Entry(police, width=21)
    en_search_code.grid(row=1, column=2, columnspan=4)
    lb_search_address = tk.Label(police, text="جستجو با مکان کنونی\nمامور راهنمایی رانندگی", fg="darkgreen")
    lb_search_address.grid(row=1, column=4, columnspan=2)
    en_search_address = tk.Entry(police, width=21)
    en_search_address.grid(row=1, column=5, columnspan=2)
    btn_submit_police = tk.Button(police, text="جستجو", command=search_police, fg="darkgreen", bd=0)
    btn_submit_police.grid(row=2, column=6, columnspan=9)
    lb_result_search_police = tk.Label(police, text="پنل ماموران راهنمایی رانندگی شهر اهواز", fg="darkgreen")
    lb_result_search_police.grid(row=2, columnspan=8, pady=5)

    width = 7
    height = 23
    cell_p = {}
    for i in range(width):
        for j in range(3, height):
            b = tk.Entry(police, width=22)
            b.grid(row=j, column=i)
            cell_p[(j, i)] = b

    cell_p[(3, 6)].insert(0, "نام و نام خانوادگی مامور")
    cell_p[(3, 5)].insert(0, "کد ملی مامور راهنمایی ")
    cell_p[(3, 4)].insert(0, "مجموع غیبت مامور/ساعت")
    cell_p[(3, 3)].insert(0, "مجموع حضور مامور/ساعت")
    cell_p[(3, 2)].insert(0, "وضعیت کنونی حاضر/غایب")
    cell_p[(3, 1)].insert(0, "چهارراه که مامور حاضراست")
    cell_p[(3, 0)].insert(0, "چهارراه شیفت بعدی مامور")

    for i in range(width):
        cell_p[(3, i)].config(state='disable')

    for j in range(3, height):
        cell_p[(j, 6)].bind('<KeyPress>', field_name_police)
    for j in range(3, height):
        cell_p[(j, 5)].bind('<KeyPress>', field_national_code_police)

    lb_shift_add = tk.Label(police, text="اضاف کردن شیفت برای\nمامور راهنمایی رانندگی", fg="darkgreen")
    lb_shift_add.grid(row=23, columnspan=5, pady=3)
    en_shift = tk.Entry(police, width=21)
    en_shift.grid(row=23, columnspan=7)
    btn_police_shift = tk.Button(police, text="اضافه کردن تا سقف پنج شیفت", command=add_shift, bd=0, fg="darkgreen")
    btn_police_shift.grid(row=23, column=3, columnspan=6, ipadx=32)
    lb_code_intersection = tk.Label(police, text="کد چهارراه", fg="darkgreen")
    lb_code_intersection.grid(row=23, column=4, columnspan=3, rowspan=2)
    en_code_intersection = tk.Entry(police, width=20)
    en_code_intersection.grid(row=23, column=4, rowspan=2)
    shift_box = tk.Listbox(police, width=44)
    shift_box.grid(row=24, columnspan=6, pady=10)
    en_key_shift = tk.Entry(police)
    en_key_shift.grid(row=24, column=4)
    lb_ntc_code_for_shift = tk.Label(police, text="کد ملی", fg="darkgreen")
    lb_ntc_code_for_shift.grid(row=24, column=4, columnspan=3)

    police.bind('<KeyPress>', send_information_police)
    clock_updater_police()
    police.mainloop()
    police.after_cancel(police_after)


"""
Basic actions on the panel intersection
send information for data base
search and update table intersection
"""


def send_information_intersection(event):
    global name_intersection_city, state_intersection, mode_ns, mode_ew, time_ns, time_ew, idx_i
    if event.keycode == 13:
        idx_i += 1
        if state_intersection == "1":
            CP.cp_add_intersection(name_intersection_city, int(state_intersection), int(mode_ns), int(mode_ew), idx_i,
                                   int(time_ns), int(time_ew))

        elif state_intersection == "0":
            CP.cp_add_intersection(name_intersection_city, int(state_intersection), int(mode_ns), int(mode_ew), idx_i)

        """
        refresh fields in table for new adding
        """
        name_intersection_city = ""
        state_intersection = ""
        mode_ns = ""
        mode_ew = ""
        time_ns = ""
        time_ew = ""


def search_intersection():
    # global lb_result_search_intersection, entry_search_key_cross, entry_search_name_cross
    result = None
    s_name = entry_search_name_cross.get()
    s_key = entry_search_key_cross.get()
    if s_key != "":
        result = CP.cp_get_intersection_with_key(int(s_key))

    elif s_name != "":
        result = CP.cp_get_intersection_with_name(s_name)

    if result is None:
        result_search = "چهار راهی با این مشخصه موجود نمی باشد"
    else:
        result_search = next(result)
    lb_result_search_intersection.config(text=result_search)


def update_table_intersection():
    if CP.control_intersections.intersections.len > 0:
        for intersection in CP.control_intersections.intersections.table:
            if isinstance(intersection, CP.control_intersections.intersections.DNode):
                if intersection.value == "deleted":
                    return
                else:
                    if intersection.value.str1.counter == 0 or intersection.value.str2.counter == 0:
                        intersection.value.str1.counter = intersection.value.time_ew
                        intersection.value.str2.counter = intersection.value.time_ns
                        if intersection.value.state == 0:
                            # red = 1, green = 0
                            # str1 = 0 : شرق غرب, str2 = 1 : شمال جنوب
                            if intersection.value.mode_ew == 1:
                                intersection.value.count_car += c_light(intersection.key, 1, 1)
                                c_light(intersection.key, 0, 0)
                            elif intersection.value.mode_ew == 0:
                                intersection.value.count_car += c_light(intersection.key, 0, 1)
                                c_light(intersection.key, 1, 0)
                            intersection.value.automatic_control()

                        elif intersection.value.state == 1:
                            if intersection.value.mode_ew == 0:
                                intersection.value.count_car += c_light(intersection.key, 0, 1)
                                c_light(intersection.key, 1, 0)
                            elif intersection.value.mode_ew == 1:
                                intersection.value.count_car += c_light(intersection.key, 1, 1)
                                c_light(intersection.key, 0, 0)
                            intersection.value.manual_control()

                    intersection.value.str1.counter -= 1
                    intersection.value.str2.counter -= 1

                    cell_i[(intersection.value.idx, 7)].delete(0, "end")
                    cell_i[(intersection.value.idx, 7)].insert(0, f"{intersection.value.name}")
                    cell_i[(intersection.value.idx, 6)].delete(0, "end")
                    cell_i[(intersection.value.idx, 6)].insert(0, f"{intersection.value.key}")
                    cell_i[(intersection.value.idx, 5)].delete(0, "end")
                    cell_i[(intersection.value.idx, 5)].insert(0, f"{intersection.value.state}")
                    cell_i[(intersection.value.idx, 4)].delete(0, "end")
                    cell_i[(intersection.value.idx, 4)].insert(0, f"{intersection.value.count_car}")
                    cell_i[(intersection.value.idx, 3)].delete(0, "end")
                    cell_i[(intersection.value.idx, 3)].insert(0, f"{intersection.value.mode_ns}")
                    cell_i[(intersection.value.idx, 2)].delete(0, "end")
                    cell_i[(intersection.value.idx, 2)].insert(0, f"{intersection.value.str2.counter}")
                    cell_i[(intersection.value.idx, 1)].delete(0, "end")
                    cell_i[(intersection.value.idx, 1)].insert(0, f"{intersection.value.mode_ew}")
                    cell_i[(intersection.value.idx, 0)].delete(0, "end")
                    cell_i[(intersection.value.idx, 0)].insert(0, f"{intersection.value.str1.counter}")
            else:
                continue


"""
Impact event functions with field name 
global values intersection with values inputs updating 
"""


def field_name_intersection(event):
    global name_intersection_city
    name_intersection_city += event.char


def field_state_intersection(event):
    global state_intersection
    state_intersection += event.char


def field_mode_ew(event):
    global mode_ew
    mode_ew += event.char


def field_mode_ns(event):
    global mode_ns
    mode_ns += event.char


def field_time_ns(event):
    global time_ns
    time_ns += event.char


def field_time_ew(event):
    global time_ew
    time_ew += event.char


"""
Basic actions on the panel police
send information for data base
search and update table intersection
"""


def send_information_police(event):
    global name_police, ntc_police, idx_p  # cell_p  CP
    if event.keycode == 13:
        idx_p += 1
        CP.control_polices.add_police(name_police, int(ntc_police), time, " سه میلیون تومان ", idx_p)
        cell_p[(idx_p, 4)].insert(0, "0")
        cell_p[(idx_p, 3)].insert(0, "0")
        cell_p[(idx_p, 2)].insert(0, "0")
        cell_p[(idx_p, 1)].insert(0, "تعریف نشده")
        cell_p[(idx_p, 0)].insert(0, "تعریف نشده")
        name_police = ""
        ntc_police = ""


def update_table_police():
    # global cell_p
    if CP.control_polices.polices.len > 0:
        for police_node in CP.control_polices.polices.table:
            if isinstance(police_node, CP.control_polices.polices.DNode):
                if police_node.value == "deleted":
                    continue
                else:
                    first_location = police_node.value.first_location()
                    if first_location is not None:
                        cell_p[police_node.value.idx, 1].delete(0, "end")
                        cell_p[police_node.value.idx, 1].insert(0, first_location.intersection_shift)
                    else:
                        cell_p[police_node.value.idx, 1].delete(0, "end")
                        cell_p[police_node.value.idx, 1].insert(0, "تعریف نشده")
                    next_location = police_node.value.next_location()
                    if next_location is not None:
                        cell_p[police_node.value.idx, 0].delete(0, "end")
                        cell_p[police_node.value.idx, 0].insert(0, next_location.intersection_shift)
                    else:
                        cell_p[police_node.value.idx, 0].delete(0, "end")
                        cell_p[police_node.value.idx, 0].insert(0, "تعریف نشده")

                    if first_location is not None and first_location.clock_time == counter:
                        c_sms(police_node.value.national_code, first_location.intersection_shift)
                    if first_location is not None and counter == (first_location.time_shift * 60 * 60):
                        attendance(police_node.value.national_code, first_location.intersection_shift)
                    if first_location is not None and counter == (first_location.next_time_shift * 60 * 60):
                        end_shift = police_node.value.del_shift()
                        messagebox.showinfo("پیغام تمام شدن شیفت", f"{next(end_shift)}")

                    cell_p[police_node.value.idx, 4].delete(0, "end")
                    cell_p[(police_node.value.idx, 4)].insert(0, police_node.value.absence)
                    cell_p[police_node.value.idx, 3].delete(0, "end")
                    cell_p[(police_node.value.idx, 3)].insert(0, police_node.value.attendance)
                    cell_p[(police_node.value.idx, 2)].delete(0, "end")
                    cell_p[(police_node.value.idx, 2)].insert(0, police_node.value.state)
            else:
                continue


def search_police():
    # global lb_result_search_police, en_search_address, en_search_code, en_search_name
    result = None
    s_address = en_search_address.get()
    s_name = en_search_name.get()
    s_ntc = en_search_code.get()
    if s_ntc != "":
        result = CP.cp_get_police_with_key(int(s_ntc))
    elif s_name != "":
        result = CP.cp_get_police_with_name(s_name)
    elif s_address != "":
        result = CP.cp_get_intersection_with_key(int(s_address))
        # result = CP.cp_get_intersection_with_name(s_address)
        if result is None:
            result_search = "چهار راهی با این کد در سیستم ثبت نشده است"
        elif result.police is None:
            result_search = "در این چهار راه پلیسی حضور ندارد"
        else:
            result_search = f" {result.police} در این چهار راه حضور دارد "
        lb_result_search_police.config(text=result_search)
        return
    if result is None:
        result_search = "پلیسی با این مشخصه ثبت نشده"
    else:
        result_search = next(result)
    lb_result_search_police.config(text=result_search)


def add_shift():
    # global en_shift, en_key_shift, en_code_intersection, shift_box
    ntc_code = en_key_shift.get()
    if ntc_code == "":
        messagebox.showwarning("!هشدار خالی بودن فرم", "قیلد کد ملی مامور راهنمایی رانندگی نمی تواند خالی باشد")
        return
    time_sh = en_shift.get()
    if time_sh == "":
        messagebox.showwarning("!هشدار خالی بودن فرم", "فیلد تعیین شیفت مامور راهنمایی رانندگی نمی تواند خالی باشد")
        return
    key_intersection = en_code_intersection.get()
    if key_intersection == "":
        messagebox.showwarning("!هشدار خالی بودن فرم", "فیلد کد چهار راه مورد نظر برای تعیین شیفت نمی تواند خالی باشد")
        return
    result_search = CP.cp_search_intersection_with_key(int(key_intersection))
    if not result_search:
        messagebox.showerror("خطای پایگاه داده ایی", "همچین چهار راهی با این کد ثبت نشده است")
        return
    obj_police = CP.cp_get_police_with_key(int(ntc_code))
    if obj_police is not None:
        result = obj_police.add_shift(int(time_sh), int(key_intersection))
    else:
        messagebox.showerror("خطای پایگاه داده ایی", "پلیسی با این کد ملی در سیستم ثبت نشده است")
        return
    if result[0]:
        shift_box.insert(0, next(result[1]))
    else:
        if result[1] == -1:
            messagebox.showerror("سرریز داده های ورودی",
                                 "بیشتر از حد مجاز برای مامور راهنمایی رانندگی شیفت تایین کرده اید")
        elif result[1] == -2:
            messagebox.showerror("خطای داده های ورودی", "یک مامور پلیس نمی تواند در حین واحد در "
                                                        "یک ساعت در دو مکان باشد")


def clear_shift_box():
    if counter == 0:
        shift_box.delete(0, "end")


"""
Impact event functions with field name 
global values police with values inputs updating 
"""


def field_national_code_police(event):
    global ntc_police
    ntc_police += event.char


def field_name_police(event):
    global name_police
    name_police += event.char


"""
clock updater: Its job is to update the elements of the page after each clock
"""


def clock_updater_login():
    global app_after
    date.config(text=f"تاریخ سیستم: {time}")
    app_after = app.after(20, clock_updater_login)


def clock_updater_home():
    global home_after
    date_home.config(text=f"تاریخ سیستم: {time}")
    home_after = home.after(20, clock_updater_home)


def clock_updater_intersection():
    global cross_after
    date_intersection.config(text=f"تاریخ سیستم: {time}")
    cross_after = cross.after(20, clock_updater_intersection)


def clock_updater_police():
    global police_after, en_shift
    date_polices.config(text=f"تاریخ سیستم: {time}")
    # if 8 <= hour < 10 or 14 <= hour < 16:
    #     en_shift.config(state='normal')
    # else:
    #     en_shift.config(state='disable')
    police_after = police.after(20, clock_updater_police)


with open('arman.simi', 'wb') as file:
    pickle.dump(CP.control_intersections.intersections.table, file)


# print(result_file)


def thread_app():
    while True:
        if app:
            pass
        else:
            pass


t = Thread(name="App", target=thread_app)

end_perfCounter = perf_counter()
end_processTime = process_time()

print("perf counter:", end_perfCounter - start_perfCounter)
print("process time:", end_processTime - start_processTime)
