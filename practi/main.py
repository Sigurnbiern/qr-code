from tkinter import *
from tkinter import messagebox
import psycopg2
from config import host, user, password, db_name
import qrcode


root = Tk()



def Btn_Click_Enter():
    Mid_Name = Entry_Mid_Name.get()
    Sur_Name = Entry_Sur_Name.get()
    Full_Name = Entry_Full_Name.get()
    Group = Entry_Gruop.get()

    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        
        
        with connection.cursor() as cursor:
            cursor.execute(
                f"Insert into Студентики(Фамилия, Имя, Отчество, Группа) values('{Mid_Name}', '{Sur_Name}', '{Full_Name}', '{Group}');"
            )
            connection.commit()
            messagebox.showinfo(message='Сохранено')
            
            cursor.execute(
                f"select id from Студентики where id = (select max(id) from Студентики);"
            )
            Id_Student = cursor.fetchone()
            print(f'id: {Id_Student[0]}')

        
        

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            
            connection.close()
            print('[INFO] Postgeawff conn closed')


    
    filename = f"{Id_Student[0]}, {Mid_Name}, {Sur_Name}, {Group}.png"
    # генерируем qr-код
    img = qrcode.make(Id_Student[0])
    # сохраняем img в файл
    img.save(filename)


root.title('Заполнение БД')
root.geometry('200x250')
root.resizable(width=False, height=False)


frame = Frame(root)
frame.place(relwidth=1, relheight=1)



Label_Mid_Name = Label(frame, text='Фамилия:')
Label_Mid_Name.place(x=10, y=10)
Entry_Mid_Name = Entry(root, bg='#B0C4DE')
Entry_Mid_Name.place(x=70, y=10)

Label_Sur_Name = Label(frame, text='Имя:')
Label_Sur_Name.place(x=10, y=50)
Entry_Sur_Name = Entry(root, bg='#B0C4DE')
Entry_Sur_Name.place(x=45, y=50)

Label_Full_Name = Label(frame, text='Отчество:')
Label_Full_Name.place(x=10, y=100)
Entry_Full_Name = Entry(root, bg='#B0C4DE')
Entry_Full_Name.place(x=70, y=100)

Label_Gruop = Label(frame, text='Группа:')
Label_Gruop.place(x=10, y=150)
Entry_Gruop = Entry(root, bg='#B0C4DE')
Entry_Gruop.place(x=60, y=150)

Button_Enter = Button(root, text='Сохранить', bg='#B0C4DE', command=Btn_Click_Enter)
Button_Enter.place(x=10, y=200)



root.mainloop()