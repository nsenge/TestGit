import tkinter as tk
from tkinter import messagebox
import math

def on_calculer():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        
        # Calcul du discriminant
        discriminant = b**2 - 4*a*c
        # Si le discriminant est négatif, il n'y a pas de solution réelle
        if discriminant < 0:
            messagebox.showinfo("Résultat", "L'équation n'a pas de solution réelle.")
        # Calcul des solutions
        elif discriminant == 0:
            # Calcul de la solution unique
            x = -b / (2*a)
            messagebox.showinfo("Résultat", f"L'équation a une racine double x1=x2={x}")
        else:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            messagebox.showinfo("Résultat", f"Les solutions de l'équation sont x1={x1} et x2={x2}")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des coefficients valides.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Équation du second degré")

# Centrer la fenêtre au milieu de l'écran
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
# Ajouter une image de fond à la fenêtre principale
background_image = tk.PhotoImage(file="C:\\Users\\Staniher\\Pictures\\compress_image.png")

background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Entrées pour les coefficients a, b, et c

label_a = tk.Label(root, text="Saisir la valeur de a:", bg="white")
label_a.pack()
entry_a = tk.Entry(root)
entry_a.pack()

label_b = tk.Label(root, text="Saisir la valeur de b:", bg="white")
label_b.pack()
entry_b = tk.Entry(root)
entry_b.pack()

label_c = tk.Label(root, text="Saisir la valeur de c:", bg="white")
label_c.pack()
entry_c = tk.Entry(root)
entry_c.pack()

# Ajouter une couleur de fond au bouton "Calculer"
button_calculer = tk.Button(root, text="Calculer", command=on_calculer, bg="blue", fg="white")
button_calculer.pack(pady=10)

# Boucle principale Tkinter
root.mainloop()
