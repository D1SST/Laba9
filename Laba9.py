from tkinter import*
from tkinter import messagebox
import sqlite3

con = sqlite3.connect('userdata.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    login text, 
                    password text
                )
            ''')
con.commit()

class SignupLoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Окно Авторизации/Регистрации")
        master.geometry("550x400")
        master["bg"] = "#B3E5FC"

        self.login_label = Label(master, text="Введите ваш логин:")
        self.login_label.place(x=145, y=90)
        self.login_entry = Entry(master)
        self.login_entry.place(x=260, y=90)

        self.password_lable = Label(master, text = "Введите пароль(не менее 6 символов):")
        self.password_lable.place(x=38, y=130)
        self.password_entry = Entry(master)
        self.password_entry.place(x=260, y=130)

        self.submit_button = Button(master, cursor="hand2", relief=RAISED, activeforeground="red", text="Войти/Зарагестрироваться", command=self.submit)
        self.submit_button.place(x=200, y=170)

    def submit(self):
        check_counter = 0
        if self.login_entry.get() == "":
            messagebox.showerror(title="ОШИБКА", message="Поле логина не может быть пустым")
        else:
            check_counter += 1
        if self.password_entry.get() == "":
            messagebox.showerror(title="ОШИБКА", message="Поле пароля не может быть пустым")
        else:
            check_counter += 1
        if self.login_entry.get() == self.password_entry.get():
            messagebox.showerror(title="ОШИБКА", message="Логин и пароль не должны совпадать")
        else:
            check_counter += 1
        if len(self.password_entry.get()) < 6:
            messagebox.showinfo(title="УВЕДОМЛЕНИЕ", message="Пароль слишком короткий")
        else:
            check_counter += 1

        def check_user(login):
            conn = sqlite3.connect('userdata.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE login=?", (login,))
            result = cursor.fetchone()
            conn.close()
            return result is not None

        def check_pass(password):
            conn = sqlite3.connect('userdata.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE password=?", (password,))
            result = cursor.fetchone()
            conn.close()
            return result is not None

        if check_counter == 4:
            login = self.login_entry.get()
            password = self.password_entry.get()
            if check_user(login):
                if check_pass(password):
                    messagebox.showinfo(title="УВЕДОМЛЕНИЕ", message="Вы вошли в аккаунт.")
                else:
                    messagebox.showerror(title="ОШИБКА", message="Пользователь с таким логином уже существует!")
            else:
                try:
                    con = sqlite3.connect('userdata.db')
                    cur = con.cursor()
                    cur.execute("INSERT INTO users VALUES (:login, :password)", {
                                    'login': self.login_entry.get(),
                                    'password': self.password_entry.get()

                    })
                    con.commit()
                    messagebox.showinfo(title = "Уведомление.", message = "Регистрация пройдена успешно.")
                except Exception as ep:
                    messagebox.showerror("", ep)

root = Tk()
root.minsize(550, 400)
root.maxsize(550, 400)
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2
h = h // 2
w = w - 275
h = h - 250
root.geometry(f'550x400+{w}+{h}')
signup_login_window = SignupLoginWindow(root)
root.mainloop()