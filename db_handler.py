class db_handler:
    
    def __init__(self, con):
        self.user = None
        self.con = con

    def create_new_user(self, email, name, password):
        cursor = self.con.cursor()
        cursor.execute("""INSERT INTO bruker (epostadresse, navn, passord)
                        VALUES (:email, :name, :password)""", {"email": email, "password": password, "name": name})
        self.con.commit()

    def login(self, email, password):
        print("Logger inn...")
        cursor = self.con.cursor()
        cursor.execute("""SELECT brukerID, epostadresse, navn, passord 
                        FROM bruker
                        WHERE epostadresse = :email AND passord = :password""", {"email": email, "password": password})
        self.user = cursor.fetchone()

    def new_coffee_review(self, distillery, coffee_name, points, notes, date):
        cursor = self.con.cursor()
        cursor.execute("""SELECT kaffeID
        FROM ferdigbrentKaffe
        WHERE navn = :coffee_name AND kaffebrennerinavn = :distillery
        """, {"coffee_name": coffee_name, "distillery": distillery})
        coffee_id = cursor.fetchone()
        sql_string = f"""INSERT INTO kaffesmaking
                VALUES (:brukerID, :kaffeID, :notes, :points, :date)
        """
        cursor.execute(sql_string, {"notes": notes, "points": points, "date": date, "kaffeID": coffee_id[0], "brukerID": self.user[0]})
        self.con.commit()
        print("Lagt til kaffesmaking")
        print()

    def view_top_list(self):
        cursor = self.con.cursor()
        sql_string = """SELECT bruker.navn, COUNT(*)
        FROM kaffesmaking
        LEFT JOIN bruker ON bruker.brukerID = kaffesmaking.brukerID
        GROUP BY navn
        ORDER BY COUNT(*) DESC
        """
        cursor.execute(sql_string)
        return cursor.fetchall()


    # mest for pengene
    # høyest gjennomsnittscore kontra pris
    # sorter synkende
    # inneholde brennerinavn, kaffenavn pris, gjennomsnittscore for hver kaffe
    def find_most_valuable(self):
        cursor = self.con.cursor()
        sql_string = """SELECT ferdigbrentKaffe.navn, ferdigbrentKaffe.kaffebrennerinavn, ferdigbrentKaffe.kgpris_nok, AVG(kaffesmaking.poengsum)
        FROM ferdigbrentKaffe
        LEFT JOIN kaffesmaking ON ferdigbrentKaffe.kaffeID = kaffesmaking.kaffeID
        GROUP BY ferdigbrentKaffe.navn
        ORDER BY AVG(kaffesmaking.poengsum)/ferdigbrentKaffe.kgpris_nok DESC
        """
        cursor.execute(sql_string)
        return cursor.fetchall()
    
    def description_search(self, search_word):
        complete_search_word = f"%{search_word}%"
        cursor = self.con.cursor()
        sql_string = """SELECT ferdigbrentKaffe.navn, ferdigbrentKaffe.kaffebrennerinavn
        FROM ferdigbrentKaffe
        LEFT JOIN kaffesmaking ON ferdigbrentKaffe.kaffeID = kaffesmaking.kaffeID
        WHERE ferdigbrentKaffe.beskrivelse LIKE ? OR kaffesmaking.smaksnotater LIKE ?"""
        cursor.execute(sql_string, (complete_search_word, complete_search_word))
        return cursor.fetchall()


    # må ha med kaffegård, ferdigbrentkaffe, kaffeparti
    def country_search(self, country, washed):
        if washed == "ja":
            sql_string = """SELECT ferdigbrentKaffe.navn, ferdigbrentKaffe.kaffebrennerinavn
            FROM ferdigbrentKaffe
            LEFT JOIN kaffeparti ON ferdigbrentKaffe.kaffepartiID = kaffeparti.kaffepartiID
            LEFT JOIN kaffegård ON kaffeparti.kaffegårdID = kaffegård.kaffegårdID
            LEFT JOIN foredlingsmetode ON kaffeparti.foredlingsmetodeID = foredlingsmetode.foredlingsmetodeID
            WHERE kaffegård.land = ? AND foredlingsmetode.navn = 'Vasket'
            """
        else:
            sql_string = """SELECT ferdigbrentKaffe.navn, ferdigbrentKaffe.kaffebrennerinavn
            FROM ferdigbrentKaffe
            LEFT JOIN kaffeparti ON ferdigbrentKaffe.kaffepartiID = kaffeparti.kaffepartiID
            LEFT JOIN kaffegård ON kaffeparti.kaffegårdID = kaffegård.kaffegårdID
            LEFT JOIN foredlingsmetode ON kaffeparti.foredlingsmetodeID = foredlingsmetode.foredlingsmetodeID
            WHERE kaffegård.land = ? AND foredlingsmetode.navn != 'Vasket'
            """

        cursor = self.con.cursor()
        cursor.execute(sql_string, (country,))
        return cursor.fetchall()
    