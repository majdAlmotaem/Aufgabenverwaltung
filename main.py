#datenbank verbinden 
import pymysql

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
    add_title = input('Geben Sie ein Title für Ihren Task....\t')
    add_beschreibung =  input('Geben Sie eine Beschreibung für Ihren Task....\t')
    add_datum = input('Example "Year-Month-Day"')
    #sql add query
    sql_query = 'INSERT INTO aufgaben (`Title`, `Beschreibung`, `Datum`) VALUES (%s, %s, %s)'
    cursor.execute(sql_query, (add_title, add_beschreibung, add_datum))
    connection.commit()

#Aufgaben anzeigen
def show_tasks():
    sql_query = 'SELECT * FROM aufgaben'
    cursor.execute(sql_query)
    tasks = cursor
    for task in tasks:
        print(task)

#Aufgaben bearbeiten
def edit_task():
    title_auswahl = input('Welche Aufgabe möchten Sie bearbeiten?(Geben Sie Title der Aufgabe ein)\t')
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
    title = input('Welcher Task möchten Sie löschen?(Geben Sie Title der Aufgabe ein)\t ')
    check_query = 'SELECT * FROM aufgaben WHERE Title = %s'
    cursor.execute(check_query, (title))
    existing_task = cursor.fetchone()
    if existing_task:
        sql_query = 'DELETE from aufgaben where `Title`= %s'
        cursor.execute(sql_query, (title))
        connection.commit()
        print('Aufgabe erfolgreich bearbeitet!')
    else:
        print('Sie haben falschen Title eingegeben')

#Menü
print("Wählen Sie eine Option aus...")
print(' 1. Add Task\n 2. Show Tasks\n 3. Edit Task\n 4. Delete Task')
option_auswahl = input()


#Auswahl bestätigen
if option_auswahl == '1': #add task
    add_task()
elif option_auswahl == '2': #Show Tasks
    show_tasks()
elif option_auswahl == '3': #Edit tasks
    edit_task()
elif option_auswahl == '4': #Delete task
    delete_task()
else:
    print('Üngultige Eingabe!')

    
    
connection.close()