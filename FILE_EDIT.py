
from tkinter import Button,END,Tk,Toplevel,Text

def edit_text_file():
    filename = "BestShot_testName.txt"

    # Read the current content of the file with UTF-8 encoding
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        content = ""

    # Create the popup window
    root = Tk()
    root.withdraw()  # Verstecke das Hauptfenster

    popup = Toplevel(root)
    popup.title("Edit File")

    # Create a Text widget with UTF-8 encoding support
    text_box = Text(popup, wrap='word', font=('Arial', 12))
    text_box.insert(END, content)
    text_box.pack(expand=True, fill='both')

    def save_and_close():
        saved = save_content(text_box, filename, popup)
        if saved:
            root.quit()  # Beende die Tkinter-Hauptloop nach dem Speichern

    # Create a Save button
    save_button = Button(popup, text="Save", command=save_and_close)
    save_button.pack()

    # Start the main loop for the popup window
    popup.mainloop()

    # Determine the return value based on user action
    if popup.winfo_exists():  # Wenn das Popup-Fenster noch existiert (nicht geschlossen wurde)
        return False  # Rückgabe, dass der Benutzer nicht gespeichert hat
    else:
        return True  # Rückgabe, dass der Benutzer gespeichert hat

def save_content(text_box, filename, popup):
    # Get the content from the text box
    new_content = text_box.get("1.0", END)

    # Process the content: split, strip, remove duplicates, sort
    lines = new_content.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    lines = list(set(lines))  # Remove duplicates
    lines.sort(key=str.lower)  # Sort ignoring case

    sorted_content = "\n".join(lines)

    # Write the sorted content back to the file with UTF-8 encoding
    with open(filename, "w", encoding="utf-8") as file:
        file.write(sorted_content)

    # Close the popup window
    popup.destroy()

    return True  # Signalisiert, dass der Inhalt erfolgreich gespeichert wurde
