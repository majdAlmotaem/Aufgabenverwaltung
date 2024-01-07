#datenbank verbinden 
from tkinter import *
import pymysql

#Tkinter erstellen
root = Tk()
root.geometry("1000x750")
root.title("Aufgabenverwaltung")
root.configure(bg="black")


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='', 
    db='Aufgaben',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

#Aufgaben hinzufügen
def add_task():
    add_title = add_task_title.get("1.0", "end")
    add_beschreibung =  add_task_beschreibung.get("1.0", "end")
    add_datum = add_task_datum.get("1.0", "end")
    # Check if all fields are filled before adding the task
    if add_title and add_beschreibung and add_datum:
        sql_query = 'INSERT INTO aufgaben (`Title`, `Beschreibung`, `Datum`) VALUES (%s, %s, %s)'
        cursor.execute(sql_query, (add_title, add_beschreibung, add_datum))
        connection.commit()
        # clear entry fields
        add_task_title.delete(1.0, END)
        add_task_beschreibung.delete(1.0, END)
        add_task_datum.delete(1.0, END)
        
        show_tasks()

#Aufgaben anzeigen
def show_tasks():
    cursor.execute('SELECT * FROM aufgaben')
    tasks = cursor.fetchall()
    i = 1
    for task in tasks:
        for j, key in enumerate(['Id','Title', 'Beschreibung', 'Datum']):
            e = Entry(fr2, width='40', fg='navy', font=('Arial', 10, 'bold'), justify="center")
            e.grid(row=i, column=j)
            e.insert(END, task[key])
            Label(fr2, text='Id', font=('Arial', 10)).grid(row=0, column=0)
            Label(fr2, text='Title', font=('Arial', 10)).grid(row=0, column=1)
            Label(fr2, text="Beschreibung", font=('Arial', 10)).grid(row=0, column=2)
            Label(fr2, text="Datum", font=('Arial', 10)).grid(row=0, column=3)
        i += 1


#Aufgaben bearbeiten
def edit_task():
    title_auswahl = input('Welche ausgabe möchten Sie bearbeiten?(Geben Sie Title der Aufgabe ein)\t')
    check_query = 'SELECT * FROM aufgaben WHERE Title = %s'
    cursor.execute(check_query, (title_auswahl,))
    existing_task = cursor.fetchone()
    if existing_task:
        changes = input('Geben Sie neue Beschreibung ein\n')
        sql_query = 'UPDATE aufgaben SET Beschreibung = %s WHERE Title = %s'
        cursor.execute(sql_query, (changes, title_auswahl))
        connection.commit()
        print('Aufgabe erfolgreich bearbeitet!')
    else:
        print('Sie haben falschen Title eingegeben')

#Aufgaben löschen
def delete_task():
    title = delete_task_title.get("1.0", "end").strip()
    check_query = 'SELECT * FROM aufgaben WHERE Id = %s'
    cursor.execute(check_query, (title))
    existing_task = cursor.fetchone()
    if existing_task:
        sql_query = 'DELETE from aufgaben where `Id`= %s'
        cursor.execute(sql_query, (title))
        connection.commit()
        delete_task_title.delete(1.0, END)
        show_tasks()
        print('Aufgabe erfolgreich bearbeitet!')
    else:
        print('Sie haben falschen Title eingegeben')

#title from app window
lb0 = Label(root, text="TaskSimple", fg="white", bg="black",)
lb0.config(font=("Helvetica", 30, "bold"))
lb0.pack(pady=(30,0))

#add tasks
fr1 = Frame(root, bg="black") #add tasks
lb1 = Label(fr1, text="Title eingeben", bg="black", fg="white")
add_task_title= Text(fr1,width="50", height="2" )
lb2 = Label(fr1, text="Beschreibung eingeben",bg="black", fg="white")
add_task_beschreibung= Text(fr1,width="50", height="6" )
lb3 = Label(fr1, text="Datum eingeben (Example: 2000.12.01)", bg="black", fg="white")
add_task_datum= Text(fr1,width="50", height="2")
btn1 = Button(fr1, command=add_task, text="Task hinzufügen")
fr1.pack(pady=(40,0))
lb1.pack(pady=(10,5))
add_task_title.pack()
lb2.pack(pady=(10,5))
add_task_beschreibung.pack()
lb3.pack(pady=(10,5))
add_task_datum.pack()
btn1.pack(pady=(10,0))

# Show tasks frame
fr2 = Frame(root)
show_tasks()


# Delete tasks
fr3 = Frame(root, pady=50, bg="black")
lb4 = Label(fr3, text="Task löschen (Id Eingeben)", width="50", height="2", bg="black", fg="white")
delete_task_title = Text(fr3, width="20", height="2")
btn2 = Button(fr3, command=delete_task, text="Task löschen", bg="white", fg="black")
lb4.pack()
delete_task_title.pack(pady=(0,10))
btn2.pack(pady=(5,0))
fr3.pack()

#lb_table.pack()
fr2.pack()

root.mainloop() 
    
connection.close()