from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import hashlib
import requests
import json
from json.decoder import JSONDecodeError

# Funzione per creare la tabella 'linkedin' se non esiste
def create_linkedin_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS edmodo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mail TEXT,
            password TEXT
        )
    ''')
    conn.commit()

def insert_data(conn, file_path):
    cursor = conn.cursor()
    with open(file_path, 'r', encoding='utf-8') as file:  # Modifica la codifica qui
        for line in file:
            parts = line.strip().split(':', 1)
            if len(parts) == 2:
                mail, password = parts
                cursor.execute('''
                    INSERT INTO linkedin (mail, password)
                    VALUES (?, ?)
                ''', (mail, password))
            else:
                print(f"Il formato della riga '{line}' non è corretto e verrà ignorato.")

    conn.commit()

def show_table_structure(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info('linkedin')")
    columns = cursor.fetchall()
    for column in columns:
        print(column)

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Creazione della tabella 'linkedin'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS linkedin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mail TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' e tabella 'linkedin' creati con successo.")

def ottimizza_database(conn):
    cursor = conn.cursor()

    # Compattazione del database per ridurre le dimensioni
    cursor.execute('VACUUM;')

    # Creazione di indici per migliorare le prestazioni delle query
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mail ON edmodo(mail);')

    # Verifica dello schema del database
    cursor.execute("PRAGMA table_info('edmodo')")
    columns = cursor.fetchall()
    print("Schema della tabella 'edmodo':")
    for column in columns:
        print(column)
    
    cursor.execute('VACUUM;')
    conn.commit()
    conn.close()

def cerca_password_da_email(conn, email):
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM linkedin WHERE mail = ?', (email,))
    colonneDB = cursor.fetchone()

    if colonneDB:
        print(f"La password associata all'email '{email}' è: {colonneDB[0]}")
    else:
        print(f"Nessuna password trovata per l'email '{email}'")

    conn.close()

def cercaPhone(conn, phone):
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM utenti WHERE phone = ?', (phone,))
    colonneDB = cursor.fetchall()

    if colonneDB:
       print(f"Risultati trovati per il numero di telefono '{phone}':")
       for row in colonneDB:
            print(row)
    else:
        print(f"Nessuna password trovata per l'email '{phone}'")

    conn.close()

def create_database_facebook(file_paths,db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Creazione della tabella 'dati'
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS utenti (
            phone TEXT,
            idUtente INTEGER,
            nome TEXT,
            cognome TEXT,
            sesso TEXT,
            location1 TEXT,
            location2 TEXT,
            status TEXT,
            work TEXT,
            mail TEXT,
            birthDate TEXT
        )
    ''')

    conn.commit()

    # Iterazione sui file e inserimento dei dati nel database
    for file_path in file_paths:
        with open(file_path, 'r',encoding='utf-8') as file:
            for line in file:
                data = line.strip().split(':')
                if len(data) >=11:
                    phone, idUtente, nome, cognome, sesso, location1, location2, status, work, _, mail, birthDate = data[:12]  # Escludi il campo "extra"
                    cursor.execute('''
                        INSERT INTO utenti (phone, idUtente, nome, cognome, sesso, location1, location2, status, work, mail, birthDate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (phone, idUtente, nome, cognome, sesso, location1, location2, status, work, mail, birthDate))

                else:
                    print(f"Il formato della riga '{line}' non è corretto e verrà ignorato.")

    conn.commit()
    conn.close()

def importaStockx(db_path,file_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stockx (
                    id INTEGER PRIMARY KEY,
                    uuid TEXT,
                    email TEXT,
                    username TEXT,
                    nome TEXT,
                    cognome TEXT,
                    password_hash TEXT,
                    valuta TEXT,
                    categoria_1 TEXT,
                    categoria_2 TEXT,
                    indirizzo_ip TEXT,
                    stato TEXT,
                    lingua TEXT,
                    altro TEXT,
                    altro_2 TEXT,
                    altro_3 TEXT,
                    altro_4 TEXT,
                    altro_5 TEXT,
                    altro_6 TEXT,
                    altro_7 TEXT,
                    altro_8 TEXT,
                    altro_9 TEXT,
                    altro_10 TEXT,
                    altro_11 TEXT,
                    altro_12 TEXT,
                    altro_13 TEXT,
                    altro_14 TEXT,
                    altro_15 TEXT,
                    altro_16 TEXT,
                    altro_17 TEXT,
                    altro_18 TEXT,
                    altro_19 TEXT,
                    altro_20 TEXT,
                    data_ora TEXT
                )''')
    with open(file_path, 'r',encoding='utf-8') as file:
        for line in file:
            data = line.strip().split('\t')
            uuid, email, username, nome, cognome, password_hash, valuta, categoria_1,categoria_2, indirizzo_ip, stato, lingua, altro, altro_2, altro_3, altro_4, altro_5, altro_6, altro_7, altro_8, altro_9, altro_10, altro_11, altro_12, altro_13, altro_14, altro_15, altro_16, altro_17, altro_18, altro_19, altro_20,data_ora = data
            cursor.execute('''INSERT INTO Dati (uuid, email, username, nome, cognome, password_hash, valuta, categoria_1,categoria_2, indirizzo_ip, stato, lingua, altro, altro_2, altro_3, altro_4,
                        altro_5, altro_6, altro_7, altro_8, altro_9, altro_10, altro_11, altro_12,
                        altro_13, altro_14, altro_15, altro_16, altro_17, altro_18, altro_19, altro_20,
                        data_ora) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?)''', (uuid, email, username, nome, cognome, password_hash, valuta, categoria_1,categoria_2, indirizzo_ip, stato, lingua, altro, altro_2, altro_3, altro_4,
                        altro_5, altro_6, altro_7, altro_8, altro_9, altro_10, altro_11, altro_12, altro_13, altro_14, altro_15, altro_16, altro_17, altro_18, altro_19, altro_20,data_ora))

    conn.commit()
    conn.close()

def getColonne():
    conn = sqlite3.connect('linkedin.db') 
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({'linkedin'})")
    columns = cursor.fetchall()
    print("Le colonne presenti nella tabella sono:")
    for column in columns:
        print(column[1])
    conn.close()

def ottieni_colonne_db(folder_path):
  database_columns = {}  # Struttura dati per memorizzare il titolo del DB e le colonne
  
  # Esamina ogni file nella cartella
  for file in os.listdir(folder_path):
    if file.endswith('.db'):
      db_path = os.path.join(folder_path, file)
      db_title = os.path.splitext(file)[0]  # Titolo del DB senza estensione
  
      # Connessione al database SQLite
      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()
  
      # Ottieni le tabelle presenti nel database
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
      tables = cursor.fetchall()
  
      columns = []
      # Per ogni tabella, ottieni le colonne
      for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_columns = cursor.fetchall()
        columns.extend([col[1] for col in table_columns])
      
      database_columns[db_title] = columns
      
      conn.close()
  
  return database_columns

def cercaNumero(colonneDB, numero):
    # Cartella contenente i database SQLite
    cartella_breach = "breach"

    # Itera attraverso ogni chiave nel dizionario 'colonneDB'
    for db_name, colonne in colonneDB.items():
        # Verifica se il database ha la colonna 'phone'
        if 'phone' in colonne:
            # Costruisci il percorso del file SQLite
            percorso_db = os.path.join(cartella_breach, f"{db_name}.db")

            # Connessione al database SQLite
            conn = sqlite3.connect(percorso_db)
            cursor = conn.cursor()

            # Esegui la query per cercare il numero nella colonna 'phone'
            query = f"SELECT * FROM {db_name} WHERE phone=?"
            cursor.execute(query, (numero,))
            
            # Ottieni tutti i risultati
            risultati = cursor.fetchall()

            # Chiudi la connessione al database
            conn.close()

            # Se ci sono risultati, stampa il nome del database e i risultati trovati
            if risultati:
                print(f"Trovato in '{db_name}' -> Risultati: {risultati}")
            else:
                print("non ho trovato nulla")

def cercaMail(colonneDB, mail_da_cercare):
    cartella_breach = "breach"

    risultati_totali = []

    for db_name, colonne in colonneDB.items():
        if 'mail' in colonne:
            percorso_db = os.path.join(cartella_breach, f"{db_name}.db")
            conn = sqlite3.connect(percorso_db)
            cursor = conn.cursor()

            query = f"SELECT * FROM {db_name} WHERE mail=?"
            cursor.execute(query, (mail_da_cercare,))
            
            risultati = cursor.fetchall()

            conn.close()

            if risultati:
                for record in risultati:
                    record_dict = {'Database': db_name}
                    for idx, col in enumerate(cursor.description):
                        record_dict[col[0]] = record[idx]
                    risultati_totali.append(record_dict)

    return risultati_totali

def cercaPassword(colonneDB,password):
    # Cartella contenente i database SQLite
    cartella_breach = "breach"

    # Itera attraverso ogni chiave nel dizionario 'colonneDB'
    for db_name, colonne in colonneDB.items():
        # Verifica se il database ha la colonna 'password'
        if 'password' in colonne:
            # Costruisci il percorso del file SQLite
            percorso_db = os.path.join(cartella_breach, f"{db_name}.db")

            # Connessione al database SQLite
            conn = sqlite3.connect(percorso_db)
            cursor = conn.cursor()

            # Esegui la query per cercare la password nella colonna 'password'
            query = f"SELECT * FROM {db_name} WHERE password=?"
            cursor.execute(query, (password,))
            
            # Ottieni tutti i risultati
            risultati = cursor.fetchall()

            # Chiudi la connessione al database
            conn.close()

            # Se ci sono risultati, stampa il nome del database e i risultati trovati
            if risultati:
                print(f"Trovato in '{db_name}' -> Risultati: {risultati}")
            risultati_totali = []
            if risultati:
                for record in risultati:
                    record_dict = {'Database': db_name}
                    for idx, col in enumerate(cursor.description):
                        record_dict[col[0]] = record[idx]
                    risultati_totali.append(record_dict)
            return risultati_totali
            
def passAPI(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Estrai le occorrenze della parte rimanente dell'hash
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                # Se trova corrispondenze, stampa il numero di occorrenze nei databreach
                print(f"La password è stata trovata {count} volte nei databreach.")
                return count # Termina la funzione dopo aver trovato la password

    # Se la password non è stata trovata nei databreach
    print("La password non è stata trovata nei databreach.")
    return 0

def cercaNome(colonneDB, nome):
    nomeMin = nome.lower()
    cartella_breach = "breach"

    risultati_totali = []

    for db_name, colonne in colonneDB.items():
        if 'nome' in colonne:
            percorso_db = os.path.join(cartella_breach, f"{db_name}.db")
            conn = sqlite3.connect(percorso_db)
            cursor = conn.cursor()

            query = f"SELECT * FROM {db_name} WHERE LOWER(nome)=?"
            cursor.execute(query, (nomeMin,))
            
            risultati = cursor.fetchall()
            conn.close()

            if risultati:
                for record in risultati:
                    record_dict = {'Database': db_name}
                    for idx, col in enumerate(cursor.description):
                        record_dict[col[0]] = record[idx]
                    risultati_totali.append(record_dict)

    return risultati_totali
                
def cercaCognome(colonneDB,cognome):
    # Cartella contenente i database SQLite
    cartella_breach = "breach"
    risultati_totali = []
    cognomeMin = cognome.lower()
    # Itera attraverso ogni chiave nel dizionario 'colonneDB'
    for db_name, colonne in colonneDB.items():
        # Verifica se il database ha la colonna 'cognome'
        if 'cognome' in colonne:
            # Costruisci il percorso del file SQLite
            percorso_db = os.path.join(cartella_breach, f"{db_name}.db")

            # Connessione al database SQLite
            conn = sqlite3.connect(percorso_db)
            cursor = conn.cursor()

            # Esegui la query per cercare il cognome nella colonna 'cognome'
            query = f"SELECT * FROM {db_name} WHERE LOWER(cognome)=?"
            cursor.execute(query, (cognomeMin,))
            
            # Ottieni tutti i risultati
            risultati = cursor.fetchall()

            # Chiudi la connessione al database
            conn.close()

            # Se ci sono risultati, stampa il nome del database e i risultati trovati
            if risultati:
                for record in risultati:
                    record_dict = {'Database': db_name}
                    for idx, col in enumerate(cursor.description):
                        record_dict[col[0]] = record[idx]
                    risultati_totali.append(record_dict)
    
    return risultati_totali

def cercaAll(colonneDB,nomeCognome):
    cartella_breach = "breach"
    nome, cognome = nomeCognome.split(", ")
    nome = nome.lower()
    cognome = cognome.lower()

    risultati_totali = []

    for db_name, colonne in colonneDB.items():
        if 'cognome' in colonne and 'nome' in colonne:
            percorso_db = os.path.join(cartella_breach, f"{db_name}.db")
            conn = sqlite3.connect(percorso_db)
            cursor = conn.cursor()

            query = f"SELECT * FROM {db_name} WHERE LOWER(cognome)=? AND LOWER(nome)=?"
            cursor.execute(query, (cognome, nome))

            risultati = cursor.fetchall()

            conn.close()

            if risultati:
                for record in risultati:
                    record_dict = {'Database': db_name}
                    for idx, col in enumerate(cursor.description):
                        record_dict[col[0]] = record[idx]
                    risultati_totali.append(record_dict)

    return risultati_totali

def cercaNumeroNew(colonneDB, numero):
    # Cartella contenente i database SQLite
    cartella_breach = "breach"

    # Lista per memorizzare i risultati trovati
    risultati_totali = []

    # Itera attraverso ogni chiave nel dizionario 'colonneDB'
    for db_name, colonne in colonneDB.items():
        # Verifica se il database ha la colonna 'phone'
        if 'phone' in colonne:
            # Costruisci il percorso del file SQLite
            percorso_db = os.path.join(cartella_breach, f"{db_name}.db")

            # Connessione al database SQLite
            conn = sqlite3.connect(percorso_db)
            cursor = conn.cursor()

            # Esegui la query per cercare il numero nella colonna 'phone'
            query = f"SELECT * FROM {db_name} WHERE phone=?"
            cursor.execute(query, (numero,))
            
            # Ottieni tutti i risultati
            risultati = cursor.fetchall()

            # Chiudi la connessione al database
            conn.close()

            # Se ci sono risultati, aggiungi alla lista 'risultati_totali'
            if risultati:
                for record in risultati:
                    # Dizionario per memorizzare le colonne trovate nel record
                    record_dict = {'Database': db_name}
                    for idx, col in enumerate(colonne):
                        record_dict[col] = record[idx] if idx < len(record) else None
                    risultati_totali.append(record_dict)

    return risultati_totali

def importVeloce (file_path):
    # Connessione al database SQLite (creerà un nuovo file se non esiste già)
    conn = sqlite3.connect('edmodo.db')

    # Creazione del cursore
    cursor = conn.cursor()

    # Creazione della tabella degli utenti
    cursor.execute('''CREATE TABLE IF NOT EXISTS edmodo (
                        id INTEGER PRIMARY KEY,
                        mail TEXT,
                        password TEXT
                    )''')

    # Lettura del file e inserimento dei dati nel database
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(':',1)
            if len(data) == 2:  # Controllo se ci sono esattamente due elementi nella riga
                mail, password = data
                cursor.execute("INSERT INTO edmodo (mail, password) VALUES (?, ?)", (mail, password))
            else:
                print(f"Il formato della riga '{line.strip()}' non è corretto")

    # Salvataggio delle modifiche e chiusura della connessione
    conn.commit()
    conn.close()

def create_sqlite_db_from_json(json_file):
    # Connessione al database SQLite
    conn = sqlite3.connect('twitter.db')
    cursor = conn.cursor()

    # Creazione della tabella nel database con la colonna 'mail'
    cursor.execute('''CREATE TABLE IF NOT EXISTS twitter (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        screen_name TEXT,
                        location TEXT,
                        url TEXT,
                        description TEXT,
                        protected BOOLEAN,
                        followers_count INTEGER,
                        friends_count INTEGER,
                        listed_count INTEGER,
                        created_at TEXT,
                        favourites_count INTEGER,
                        verified BOOLEAN,
                        statuses_count INTEGER,
                        is_translator BOOLEAN,
                        profile_image_url_https TEXT,
                        default_profile_image BOOLEAN,
                        translator_type TEXT,
                        mail TEXT
                    )''')

    # Lettura del file JSON e inserimento dei dati nel database
    with open(json_file, 'r') as file:
        try:
            json_data = json.load(file)
            for data in json_data:
                cursor.execute('''INSERT INTO twitter 
                                  (id, name, screen_name, location, url, description, protected, followers_count,
                                  friends_count, listed_count, created_at, favourites_count, verified, statuses_count,
                                  is_translator, profile_image_url_https, default_profile_image, translator_type, mail)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    data['id'], data['name'], data['screen_name'], data['location'], data['url'], data['description'],
                    data['protected'], data['followers_count'], data['friends_count'], data['listed_count'],
                    data['created_at'], data['favourites_count'], data['verified'], data['statuses_count'],
                    data['is_translator'], data['profile_image_url_https'], data['default_profile_image'],
                    data['translator_type'], data.get('mail', '')  # Ottieni l'email se presente, altrimenti vuoto
                ))
        except JSONDecodeError as e:
            print(f"Errore di decodifica JSON: {e}")
            print(f"Extra data trovato: {file.read()}")

    # Salvataggio delle modifiche e chiusura della connessione
    conn.commit()
    conn.close()

folder_path = "breach"
colonneDB = ottieni_colonne_db(folder_path)

#importVeloce("raw/edmodo/edmodo.txt")
#conn = sqlite3.connect('breach/edmodo.db')
#ottimizza_database(conn)


app = Flask(
    __name__,
    template_folder = 'templates',
    static_folder='static'
)

app.secret_key = 'chiave'

@app.route('/')  # '/' for the default page
def home():
	return render_template('homepage.html')

@app.route('/processa_richiesta', methods=['GET','POST'])
def processa_richiesta():
  search_query = request.form.get('search_query')
  filter_value = request.form.get('filter')
  
  risultati = []
  counterHIBPWN = None
  
  if filter_value == 'All':
    risultati=cercaAll(colonneDB,search_query)
    pass
  elif filter_value == 'E-Mail':
    risultati=cercaMail(colonneDB,search_query)
    pass
  elif filter_value == 'Phone Number':
    risultati = cercaNumeroNew(colonneDB,search_query)
    
    print(str(risultati))
    pass
  elif filter_value == 'Password':
    risultati = cercaPassword(colonneDB,search_query)
    counterHIBPWN = passAPI(search_query)

    pass
  elif filter_value == 'First Name':
    risultati=cercaNome(colonneDB, search_query)
    pass
  elif filter_value == 'Last Name':
    risultati = cercaCognome(colonneDB,search_query)
    pass
  
  if not risultati:
        messaggio_errore = "La ricerca non ha prodotto risultati."
        return render_template('risultato.html', search_query=search_query, filter_value=filter_value, messaggio_errore=messaggio_errore)
  else:
        return render_template('risultato.html', search_query=search_query, filter_value=filter_value, risultati=risultati,counterHIBPWN=counterHIBPWN)

@app.route('/processa_identikit', methods=['POST'])
def processa_identikit():
    risultati=[]
    if request.method == 'POST':
        data = request.json  # Ottieni i dati inviati come JSON
        mail = data.get('mail')  # Estrai il valore della colonna 'mail'
        phone = data.get('phone')  # Estrai il valore della colonna 'phone'

        # Fai ciò che è necessario con i valori ricevuti
        if mail:
            # Fai qualcosa con il valore della mail
            print(f"Valore della mail: {mail}")
            risultati=cercaMail(colonneDB,mail)
        
        if phone:
            # Fai qualcosa con il valore del telefono
            print(f"Valore del telefono: {phone}")
            risultati=cercaNumeroNew(colonneDB,phone)

    print(str(risultati))
    global merged_data

    for entry in risultati:
        for key, value in entry.items():
            if key not in merged_data:
                merged_data[key] = value
            else:
                if merged_data[key] != value and key != 'Database':
                    # Verifica se il valore attuale non è vuoto e unisce i valori
                    if merged_data[key] != '' and value != '':
                        merged_data[key] = f"{merged_data[key]}, {value}"
                    # Se uno dei valori è vuoto, imposta semplicemente il valore non vuoto
                    else:
                        merged_data[key] = merged_data[key] if merged_data[key] != '' else value

    return render_template("identikit.html")
    
@app.route('/identikit.html', methods=['GET','POST'])
def show_identikit():
    risultati = []
    merged_data = {}

    if request.method == 'POST':
        data = request.json  # Ottieni i dati inviati come JSON
        mail = data.get('mail')  # Estrai il valore della colonna 'mail'
        phone = data.get('phone')  # Estrai il valore della colonna 'phone'

        # Fai ciò che è necessario con i valori ricevuti
        if mail:
            # Fai qualcosa con il valore della mail
            risultati = cercaMail(colonneDB, mail)
        
        if phone:
            # Fai qualcosa con il valore del telefono
            risultati = cercaNumeroNew(colonneDB, phone)

        for entry in risultati:
            for key, value in entry.items():
                if key not in merged_data:
                    merged_data[key] = value
                else:
                    if merged_data[key] != value and key != 'Database':
                        # Verifica se il valore attuale non è vuoto e unisce i valori
                        if merged_data[key] != '' and value != '':
                            merged_data[key] = f"{merged_data[key]}, {value}"
                        # Se uno dei valori è vuoto, imposta semplicemente il valore non vuoto
                        else:
                            merged_data[key] = merged_data[key] if merged_data[key] != '' else value
        session['merged_data'] = merged_data 

        print("MergeFinale")
        print(str(merged_data))
        merged_data = session.get('merged_data', {})
        return render_template('identikit.html', merged_data=merged_data)  # Restituisce la pagina con i dati aggiornati

    if request.method == 'GET':
        merged_data = session.get('merged_data', {})
        return render_template('identikit.html', merged_data=merged_data)  # Restituisce la pagina con merged_data vuoto inizialmente
    
    merged_data = session.get('merged_data', {})
    return render_template('identikit.html', merged_data=merged_data)  # Restituisce la pagina con merged_data vuoto se non c'è alcuna corrispondenza


if __name__ == '__main__':
    app.run(debug=True)