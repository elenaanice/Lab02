def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        album= []
        with open(file_path, "r", encoding="utf-8") as file:
            #salta la riga dell'intestazione
            next(file, None)

            for riga in file:
                riga = riga.strip()
                if not riga:
                    continue

                parti=riga.split(',')
                if len(parti)<5:
                    continue

                codice = parti[0].strip()
                titolo = parti[1].strip()
                autore = parti[2].strip()
                mese = int(parti[3].strip())
                anno = int(parti[4].strip())

                #Struttura foto: lista con i dettagli della foto
                foto = [codice, titolo, autore, mese, anno]

                #Cerco se 'anno è già presente nell'album
                anno_trovato = False
                for blocco_anno in album:
                    if blocco_anno[0]==anno:
                        blocco_anno[1].append(foto)
                        anno_trovato=True
                        break

                #Se l'anno non è ancora presente, creo una nuova sotto_lista
                if not anno_trovato:
                    album.append([anno, [foto]])
        return album
    except FileNotFoundError:
        return None



def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    #Validazione del mese
    if not (1<=mese<=12):
        return None

    #Controllo codice Duplicato
    for blocco_anno in album:
        for foto in blocco_anno[1]:
            if foto[0]==codice:
                return None

    #Aggiornamento del file
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        return None

    #Inserisco nella struttura dati
    nuova_foto = [codice, titolo, autore, mese, anno]

    for blocco_anno in album:
        if blocco_anno[0]==anno:
            blocco_anno[1].append(nuova_foto)
            return nuova_foto

    album.append([anno, [nuova_foto]])
    return nuova_foto




def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    if album is None:
        return None

    for blocco_anno in album:
        for foto in blocco_anno[1]:
            if foto[0] == codice:
                return f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}"
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""

    if album is None:
        return None

    for blocco_anno in album:
        if blocco_anno[0]==anno:
            titoli = [foto[1] for foto in blocco_anno[1]]
            titoli.sort()
            return titoli

    return None




def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
