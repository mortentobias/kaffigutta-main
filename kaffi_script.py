import sqlite3
from db_handler import db_handler
from datetime import date

con = sqlite3.connect("nykaffi.db")
db = db_handler(con)

print("\nVelkommen til kaffiguttas KaffiDB:)")
print("""Du kan:
1. legge til en kaffesmaking
2. se toppliste over mest aktive brukere
3. se liste over kaffe som gir mest for pengene
4. søke etter kaffe basert på beskrivelse
5. søke etter kaffe basert på foredlingsmetode
""")

user_command = ""

while(user_command != "0"):
    while db.user == None:
        user_command = input("Har du en bruker fra før av? (ja/nei) ").lower()
        if (user_command == "ja"):
            print("\nVennligst logg inn")
            user_email = input("Skriv inn e-post: ")
            user_password = input("Skriv inn passord: ")
            db.login(user_email, user_password)
            if db.user == None:
                print("Innlogging feilet")
            else:
                print(f"Du har logget inn som {db.user[1]}")
                print()
        elif (user_command == "nei"):
            print("Oppretter ny bruker")
            email = input("Skriv inn e-post: ")
            name = input("Skriv inn navn: ")
            password = input("Skriv inn passord: ")
            db.create_new_user(email, name, password)
    
    print("""\nSkriv inn:
0 - for å avslutte programmet
1 - for å legge til en kaffesmaking
2 - for å se toppliste over mest aktive brukere
3 - for å se liste over kaffe som gir mest for pengene
4 - for å søke etter kaffe basert på beskrivelse
5 - for å søke etter kaffe basert på opprinnelsesland og foredlingsmetode
""")
    user_command = input("> ")

    if user_command == "1":
        print("Legge til kaffesmaking")
        try: 
            distillery = input("Skriv inn brenneri: ")
            coffee_name = input("Skriv inn navn på kaffe: ")
            points = int(input("Skriv inn antall poeng (0-10): "))
            notes = input("Skriv inn smaksnotater: ")
            today = date.today().strftime("%d.%m.%Y")
            db.new_coffee_review(distillery, coffee_name, points, notes, today)
        except:
            print("\nDet har skjedd en feil. Kaffesmaking ble ikke lagt til. ")
    
    elif user_command == "2":
        print("Se toppliste over mest aktive brukere")
        top_list = db.view_top_list()
        rank = 1
        for tuple in top_list:
            print(f"{rank}: {tuple[0]} | Antall kaffer smakt: {tuple[1]}")
            rank += 1
        print()
    
    elif user_command == "3":
        print("Se liste over kaffe som gir mest for pengene")
        """mest for pengene
        høyest gjennomsnittscore kontra pris
        sorter synkende
        inneholde brennerinavn, pris, gjennomsnittscore for hver kaffe
        """
        most_valuable = db.find_most_valuable()
        rank = 1
        for tuple in most_valuable:
            print(f"{rank}: {tuple[0]} | {tuple[1]} | {tuple[2]} | {tuple[3]}")
            rank += 1
        print()

    elif user_command == "4":
        search = input("Søk etter: ")
        searched = db.description_search(search_word=search)
        for tuple in searched:
            print(f"{tuple[0]} | {tuple[1]}")
    
    elif user_command == "5":
        country = input("Søk etter kaffe fra hvilket land?: ")
        washed = input("Søke etter foredlingmetode 'vasket'? (ja/nei)").lower()
        searched = db.country_search(country, washed)
        for tuple in searched:
            print(f"{tuple[0]} | {tuple[1]}")

    elif user_command == "0":
        con.close()

    else:
        print("Du skrev inn noe feil")