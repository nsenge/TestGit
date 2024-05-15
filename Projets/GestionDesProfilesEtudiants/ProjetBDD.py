#On doit installer pip install pymysql
import pymysql
import tkinter as tk
import os
import random
import string
import csv

from datetime import date,datetime
from tkinter import ttk
#pip install pillow pour installer PIL
from PIL import Image
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, Entry, filedialog

def getDateActuelle():
    return f"{date.today().month}/{date.today().day}/{date.today().year}"

def generer_caracteres_aleatoires(length=12):
    caracteres = string.ascii_lowercase
    caracteres_aleatoires = ''.join(random.choice(caracteres) for _ in range(length))
    return caracteres_aleatoires 

def connection():
    conn=pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='profile_etudiants'
    )
    return conn

def exporterExcel():
    conn=connection()
    cursor=conn.cursor()
    cursor.connection.ping()
    sql=f"SELECT * FROM etudiants ORDER BY `id` DESC"
    cursor.execute(sql)
    donneesBrutes=cursor.fetchall()
    date = str(datetime.now())
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    dateFinal = date[0:16]
    with open("etudiants_"+dateFinal+".csv",'a',newline='') as f:
        w = csv.writer(f, dialect='excel')
        w.writerow(['id','Image de Profile','Matricule','Nom','Post Nom','Téléphone','Email','Addresse','Date modification'])
        for occurence in donneesBrutes:
            w.writerow(occurence)
    print("sauvegardé: etudiants_"+dateFinal+".csv")
    conn.commit()
    conn.close()
    messagebox.showinfo("","Fichier Excel téléchargé")

def LireLesDonneesDeLaBDD():
    conn=connection()
    cursor=conn.cursor()
    cursor.connection.ping()
    sql=f"SELECT * FROM etudiants ORDER BY `id` DESC"
    cursor.execute(sql)
    resultats=cursor.fetchall()
    conn.commit()
    conn.close()
    return resultats

def renderTreeVIew(data):
    global treeFrame
    treeFrame=ttk.Frame(mainCanvas)
    treeFrame.place(x=270.0,y=130.0,width=760.0,height=535.0)

    global treeScroll
    treeScroll=ttk.Scrollbar(treeFrame)
    treeScroll.pack(side="right",fill="y")

    global treeview
    colonnes=("Matricule","Nom","Post Nom","Téléphone","Email","Addresse","Date modification")
    treeview=ttk.Treeview(treeFrame,show="headings",style="mystyle.Treeview",yscrollcommand=treeScroll.set,columns=colonnes)
    treeview.heading("Matricule",text="Matricule",anchor="w")
    treeview.heading("Nom",text="Nom",anchor="w")
    treeview.heading("Post Nom",text="Post Nom",anchor="w")
    treeview.heading("Téléphone",text="Téléphone",anchor="w")
    treeview.heading("Email",text="Email",anchor="w")
    treeview.heading("Addresse",text="Addresse",anchor="w")
    treeview.heading("Date modification",text="Date modification",anchor="w")

    treeview.column("Matricule",width=75)
    treeview.column("Nom",width=90)
    treeview.column("Post Nom",width=108)
    treeview.column("Téléphone",width=90)
    treeview.column("Email",width=150)
    treeview.column("Addresse",width=130)
    treeview.column("Date modification",width=116)
    for data in treeview.get_children():
        treeview.delete(data)
    for array in data:
        treeview.insert('',tk.END,values=array[2:],iid=array[0])
        print(array)
    treeview.place(x=0,y=0,width=745.0,height=535.0)
    treeScroll.config(command=treeview.yview)

def closeWindow(window):
    window.destroy()
    if os.path.exists("./assets/uploaded/temp.png"):
        os.remove("./assets/uploaded/temp.png")

def addWindowAssets(str):
    return f"./assets/frame1/{str}"

def editWindowAssets(str):
    return f"./assets/frame1/{str}"

def viewWindowAssets(str):
    return f"./assets/frame1/{str}"

def mainWindowAssets(str):
    return f"./assets/frame0/{str}"

def supprimerEtudiant():
    try:
        donneeSupprimer = str(treeview.item(treeview.selection()[0])['values'][0])
    except:
        messagebox.showwarning("Information", "Veuiller séléctionner une ligne de données")
        return
    decision = messagebox.askquestion("Attention", "Voulez-vous supprimer l'étudiant séléctionné?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM etudiants WHERE matricule='{str(donneeSupprimer)}'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Erreur", "Désolé, une erreur s'est produite")
            return
    print(donneeSupprimer)
    renderTreeVIew(LireLesDonneesDeLaBDD())

def modifierEtudiant():
    selectionDonneeEtudiant = [0,0,0,0,0,0]
    try:
        for i in range(0,6):
            selectionDonneeEtudiant[i] = str(treeview.item(treeview.selection()[0])['values'][i])
    except:
        messagebox.showwarning("Information", "Veuiller séléctionner une ligne de données")
        return
    print(selectionDonneeEtudiant)
    renderEditWindow(selectionDonneeEtudiant)

def voirEtudiant():
    selectionDonneeEtudiant = [0,0,0,0,0,0]
    try:
        for i in range(0,6):
            selectionDonneeEtudiant[i] = str(treeview.item(treeview.selection()[0])['values'][i])
    except:
        messagebox.showwarning("Information", "Veuiller séléctionner une ligne de données")
        return
    print(selectionDonneeEtudiant)
    renderViewWindow(selectionDonneeEtudiant)

def renderAddWindow():

    def ajoutEtudiant():
        nomDeImageProfile = f"{generer_caracteres_aleatoires()}.png"
        matricule= str(ajoutInputMatricule.get())
        nom = str(ajoutInputNom.get())
        postnom = str(ajoutInputPostnom.get())
        telephone = str(ajoutInputTelephone.get())
        email = str(ajoutInputEmail.get())
        addresse = str(ajoutInputAddresse.get())
        if (matricule == "" or matricule == " ") or (nom == "" or nom == " ") or (postnom == "" or postnom == " ") or (telephone == "" or telephone == " ") or (email == "" or email == " ") or (addresse == "" or addresse == " "):
            messagebox.showinfo("Erreur", "Veuillez compléter l'entrée vide", parent=addCanvas)
            return
        else:
            try:
                conn = connection()
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM etudiants WHERE matricule = '{matricule}'")
                if cursor.fetchone() is not None:
                    messagebox.showinfo("Erreur", "Ce Matricule existe déjà", parent=addCanvas)
                    conn.close()
                    return

                global profile_img
                profile_img = Image.open("./assets/uploaded/temp.png")
                profile_img = profile_img.resize((145, 145), resample=Image.LANCZOS)
                profile_img = profile_img.convert("RGB")
                profile_img.save(f"./assets/uploaded/{nomDeImageProfile}", format="PNG")
                if os.path.exists("./assets/uploaded/temp.png"):
                    os.remove("./assets/uploaded/temp.png")
            
                cursor.execute(f"INSERT INTO etudiants (image_profile, matricule, nom, postnom, phone, email, addresse, date_mise_a_jour) VALUES ('{nomDeImageProfile}', '{matricule}', '{nom}', '{postnom}', '{telephone}', '{email}', '{addresse}', '{getDateActuelle()}')")
                conn.commit()
                conn.close()
            except Exception as e:
                print(e)
                messagebox.showinfo("Erreur", "Une erreur s'est produite lors de l'ajout de l'étudiant", parent=addCanvas)
                return

        closeWindow(addWindow)
        renderTreeVIew(LireLesDonneesDeLaBDD())

    def setPreviewPic(filepath):
        global image
        try:
            image = PhotoImage(master=addWindow, file=filepath)
            addCanvas.create_image(112.0, 168.0, image=image)
        except Exception as e: 
            print(e)

    def selectPic():
        global filepath
        filepath = filedialog.askopenfilename(
            master=addCanvas,
            initialdir=os.getcwd(), 
            title="Sélection de l'image",
            filetypes=[("fichiers des images","*.png *.jpg *.jpeg"),]
        )
        global profile_img
        profile_img = Image.open(filepath)
        profile_img = profile_img.resize((145, 145), resample=Image.LANCZOS)
        profile_img = profile_img.convert("RGB")
        profile_img.save(f"./assets/uploaded/temp.png", format="PNG")
        setPreviewPic(f"./assets/uploaded/temp.png")

    print("Rendre la fenêtre d'ajout des Etudiants")
    addWindow = Tk()
    addWindow.title('Ajouter un Etudiant - Système de gestion des profiles des étudiants')
    addWindow.geometry("720x480")
    addWindow.configure(bg = "#FFFFFF")
    addCanvas = Canvas(addWindow,bg = "#FFFFFF",height = 480,width = 720,bd = 0,highlightthickness = 0,relief = "ridge")
    addCanvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(master=addWindow, file=addWindowAssets("image_1.png"))
    addCanvas.create_image(360.0, 264.0, image=image_image_1)
    image_image_2 = PhotoImage(master=addWindow, file=addWindowAssets("image_2.png"))
    addCanvas.create_image(360.0, 24.0, image=image_image_2)
    addCanvas.create_text(49.0, 10.0, anchor="nw", text="Ajouter Etudiant", fill="#FFFFFF", font=("Inter SemiBold", 24 * -1))
    image_image_3 = PhotoImage(master=addWindow, file=addWindowAssets("image_3.png"))
    addCanvas.create_image(28.0, 24.0, image=image_image_3)

    #input de matricule
    image_image_5 = PhotoImage(master=addWindow, file=addWindowAssets("image_5.png"))
    addCanvas.create_image(456.0, 104.0, image=image_image_5)
    entry_image_2 = PhotoImage(master=addWindow, file=addWindowAssets("entry_2.png"))
    addCanvas.create_image(455.0, 109.5, image=entry_image_2)
    ajoutInputMatricule = Entry(master=addWindow, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    ajoutInputMatricule.place(x=325.0, y=98.0, width=260.0, height=21.0)
    addCanvas.create_text(325.0, 85.0, anchor="nw", text="Matricule", fill="#000000", font=("Inter", 11 * -1))

    #input du nom
    image_image_4 = PhotoImage(master=addWindow, file=addWindowAssets("image_4.png"))
    addCanvas.create_image(457.0, 166.0, image=image_image_4)
    entry_image_1 = PhotoImage(master=addWindow, file=addWindowAssets("entry_1.png"))
    addCanvas.create_image(456.0, 171.5, image=entry_image_1)
    ajoutInputNom = Entry(master=addWindow,bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    ajoutInputNom.place(x=326.0, y=160.0, width=260.0, height=21.0)
    addCanvas.create_text(326.0, 147.0, anchor="nw", text="Nom", fill="#000000", font=("Inter", 11 * -1))

    #input du postnom
    image_image_6 = PhotoImage(master=addWindow, file=addWindowAssets("image_6.png"))
    addCanvas.create_image(457.0,230.0,image=image_image_6)
    entry_image_3 = PhotoImage(master=addWindow, file=addWindowAssets("entry_3.png"))
    addCanvas.create_image(456.0,235.5,image=entry_image_3)
    ajoutInputPostnom = Entry(master=addWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    ajoutInputPostnom.place(x=326.0,y=224.0,width=260.0,height=21.0)
    addCanvas.create_text(326.0,211.0,anchor="nw",text="Post Nom",fill="#000000",font=("Inter", 11 * -1))

    #input du téléphone
    image_image_7 = PhotoImage(master=addWindow, file=addWindowAssets("image_7.png"))
    addCanvas.create_image(166.0,294.0,image=image_image_7)
    entry_image_4 = PhotoImage(master=addWindow, file=addWindowAssets("entry_4.png"))
    addCanvas.create_image(165.0,299.5,image=entry_image_4)
    ajoutInputTelephone = Entry(master=addWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    ajoutInputTelephone.place(x=35.0,y=288.0,width=260.0,height=21.0)
    addCanvas.create_text(35.0,275.0,anchor="nw",text="Téléphone",fill="#000000",font=("Inter", 11 * -1))

    #input de l'email
    image_image_8 = PhotoImage(master=addWindow, file=addWindowAssets("image_8.png"))
    addCanvas.create_image(457.0,294.0,image=image_image_8)
    entry_image_5 = PhotoImage(master=addWindow, file=addWindowAssets("entry_5.png"))
    addCanvas.create_image(456.0,299.5,image=entry_image_5)
    ajoutInputEmail = Entry(master=addWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    ajoutInputEmail.place(x=326.0,y=288.0,width=260.0,height=21.0)
    addCanvas.create_text(326.0,275.0,anchor="nw",text="Email",fill="#000000",font=("Inter", 11 * -1))
    
    #input de l'addresse
    image_image_9 = PhotoImage(master=addWindow, file=addWindowAssets("image_9.png"))
    addCanvas.create_image(311.0, 358.0, image=image_image_9)
    entry_image_6 = PhotoImage(master=addWindow, file=addWindowAssets("entry_6.png"))
    addCanvas.create_image(310.5, 363.5, image=entry_image_6)
    ajoutInputAddresse = Entry(master=addWindow, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    ajoutInputAddresse.place(x=35.0, y=352.0, width=551.0, height=21.0)
    addCanvas.create_text(35.0,339.0,anchor="nw",text="Addresse",fill="#000000",font=("Inter", 11 * -1))

    image_image_10 = PhotoImage(master=addWindow, file=addWindowAssets("image_10.png"))
    addCanvas.create_image(166.0, 167.0, image=image_image_10)
    
    setPreviewPic("./assets/uploaded/default.png")

    button_image_2 = PhotoImage(master=addWindow, file=addWindowAssets("button_2.png"))
    selectImageBtn = Button(master=addWindow, image=button_image_2, borderwidth=0, highlightthickness=0, command=selectPic, relief="flat")
    selectImageBtn.place(x=196.0, y=215.0, width=96.0, height=25.0)

    button_image_3 = PhotoImage(master=addWindow, file=addWindowAssets("button_3.png"))
    addSubmitBtn = Button(master=addWindow, image=button_image_3, borderwidth=0, highlightthickness=0, command=ajoutEtudiant, relief="flat")
    addSubmitBtn.place(x=28.0, y=402.0, width=96.0, height=25.0)

    button_image_4 = PhotoImage(master=addWindow, file=addWindowAssets("button_4.png"))
    cancelBtn = Button(master=addWindow, image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: closeWindow(addWindow), relief="flat")
    cancelBtn.place(x=137.0, y=402.0, width=96.0, height=25.0)

    addWindow.resizable(False, False)
    addWindow.mainloop()

def renderEditWindow(selectionDonneeEtudiant):
    def modifierEtudiant():
        nomDeImageProfile = f"{generer_caracteres_aleatoires()}.png"
        idEtudiantSelectionne = selectionDonneeEtudiant[0]
        matricule = str(modifieMatriculeEtudiantInput.get())
        nom = str(modifieNomEtudiantInput.get())
        postnom = str(modifiePostnomEtudiantInput.get())
        telephone= str(modifieTelephoneEtudiantInput.get())
        email = str(modifieEmailEtudiantInput.get())
        addresse = str(modifieAddresseEtudiantInput.get())
        if (matricule == "" or matricule == " ") or (nom == "" or nom == " ") or (postnom == "" or postnom == " ") or (telephone == "" or telephone == " ") or (email == "" or email == " ") or (addresse == "" or addresse == " "):
            messagebox.showinfo("Erreur", "Veuillez compléter l'entrée vide",parent=editCanvas)
            return
        else:
            try:
                try:
                    global profile_img
                    profile_img = Image.open("./assets/uploaded/temp.png")
                    profile_img = profile_img.resize((145, 145), resample=Image.LANCZOS)
                    profile_img = profile_img.convert("RGB")
                    profile_img.save(f"./assets/uploaded/{nomDeImageProfile}", format="PNG")
                    conn = connection()
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM etudiants WHERE matricule='{matricule}' ")
                    resultat = cursor.fetchone()
                    conn.commit()
                    conn.close()
                    if os.path.exists(f"./assets/uploaded/{resultat[1]}"):
                        os.remove(f"./assets/uploaded/{resultat[1]}")
                    conn = connection()
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE etudiants SET image_profile='{nomDeImageProfile}',matricule='{matricule}',nom='{nom}',postnom='{postnom}',phone='{telephone}',email='{email}',addresse='{addresse}',date_mise_a_jour='{getDateActuelle()}' WHERE matricule='{idEtudiantSelectionne}' ")
                    conn.commit()
                    conn.close()
                except:
                    conn = connection()
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE etudiants SET matricule='{matricule}',nom='{nom}',postnom='{postnom}',phone='{telephone}',email='{email}',addresse='{addresse}',date_mise_a_jour='{getDateActuelle()}' WHERE matricule='{idEtudiantSelectionne}' ")
                    conn.commit()
                    conn.close()
                if os.path.exists("./assets/uploaded/temp.png"):
                    os.remove("./assets/uploaded/temp.png")
            except Exception as e:
                print(e)
                messagebox.showinfo("Erreur", "Une erreur est survenue",parent=editCanvas)
                return
        closeWindow(editWindow)
        renderTreeVIew(LireLesDonneesDeLaBDD())

    def setPreviewPic(filepath):
        global image
        try:
            image = PhotoImage(master=editWindow, file=filepath)
            editCanvas.create_image(112.0, 168.0, image=image)
        except Exception as e: 
            print(e)

    def selectPic():
        global filepath
        filepath = filedialog.askopenfilename(
            master=editCanvas,
            initialdir=os.getcwd(), 
            title="Selection de l'image",
            filetypes=[("Fichiers des images","*.png *.jpg *.jpeg"),]
        )
        global profile_img
        profile_img = Image.open(filepath)
        profile_img = profile_img.resize((145, 145), resample=Image.LANCZOS)
        profile_img = profile_img.convert("RGB")
        profile_img.save(f"./assets/uploaded/temp.png", format="PNG")
        setPreviewPic(f"./assets/uploaded/temp.png")

    matricule=selectionDonneeEtudiant[0]
    nom=selectionDonneeEtudiant[1]
    postnom=selectionDonneeEtudiant[2]
    telephone=selectionDonneeEtudiant[3]
    email=selectionDonneeEtudiant[4]
    addresse=selectionDonneeEtudiant[5]
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM etudiants WHERE matricule='{matricule}' ")
    resultat = cursor.fetchone()
    conn.commit()
    conn.close()

    editWindow = Tk()
    editWindow.title('Fenêtre de modification - Système de gestion des profils des étudiants')
    editWindow.geometry("720x480")
    editWindow.configure(bg = "#FFFFFF")
    editCanvas = Canvas(editWindow,bg = "#FFFFFF",height = 480,width = 720,bd = 0,highlightthickness = 0,relief = "ridge")
    editCanvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(master=editWindow, file=editWindowAssets("image_1.png"))
    editCanvas.create_image(360.0, 264.0, image=image_image_1)
    image_image_2 = PhotoImage(master=editWindow, file=editWindowAssets("image_2.png"))
    editCanvas.create_image(360.0, 24.0, image=image_image_2)
    editCanvas.create_text(49.0, 10.0, anchor="nw", text="Modifier Etudiant", fill="#FFFFFF", font=("Inter SemiBold", 24 * -1))
    image_image_3 = PhotoImage(master=editWindow, file=editWindowAssets("image_3.png"))
    editCanvas.create_image(28.0, 24.0, image=image_image_3)

    #input modifier matricule
    image_image_5 = PhotoImage(master=editWindow, file=editWindowAssets("image_5.png"))
    editCanvas.create_image(456.0, 104.0, image=image_image_5)
    entry_image_2 = PhotoImage(master=editWindow, file=editWindowAssets("entry_2.png"))
    editCanvas.create_image(455.0, 109.5, image=entry_image_2)
    modifieMatriculeEtudiantInput = Entry(master=editWindow, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    modifieMatriculeEtudiantInput.place(x=325.0, y=98.0, width=260.0, height=21.0)
    editCanvas.create_text(325.0, 85.0, anchor="nw", text="Matricule", fill="#000000", font=("Inter", 11 * -1))
    modifieMatriculeEtudiantInput.insert(0,matricule)

    #input de modification du nom
    image_image_4 = PhotoImage(master=editWindow, file=editWindowAssets("image_4.png"))
    editCanvas.create_image(457.0, 166.0, image=image_image_4)
    entry_image_1 = PhotoImage(master=editWindow, file=editWindowAssets("entry_1.png"))
    editCanvas.create_image(456.0, 171.5, image=entry_image_1)
    modifieNomEtudiantInput = Entry(master=editWindow,bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    modifieNomEtudiantInput.place(x=326.0, y=160.0, width=260.0, height=21.0)
    editCanvas.create_text(326.0, 147.0, anchor="nw", text="Nom", fill="#000000", font=("Inter", 11 * -1))
    modifieNomEtudiantInput.insert(0,nom)

    #input de modification de post nom
    image_image_6 = PhotoImage(master=editWindow, file=editWindowAssets("image_6.png"))
    editCanvas.create_image(457.0,230.0,image=image_image_6)
    entry_image_3 = PhotoImage(master=editWindow, file=editWindowAssets("entry_3.png"))
    editCanvas.create_image(456.0,235.5,image=entry_image_3)
    modifiePostnomEtudiantInput = Entry(master=editWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    modifiePostnomEtudiantInput.place(x=326.0,y=224.0,width=260.0,height=21.0)
    editCanvas.create_text(326.0,211.0,anchor="nw",text="Post Nom",fill="#000000",font=("Inter", 11 * -1))
    modifiePostnomEtudiantInput.insert(0,postnom)

    #input de modification de telephone
    image_image_7 = PhotoImage(master=editWindow, file=editWindowAssets("image_7.png"))
    editCanvas.create_image(166.0,294.0,image=image_image_7)
    entry_image_4 = PhotoImage(master=editWindow, file=editWindowAssets("entry_4.png"))
    editCanvas.create_image(165.0,299.5,image=entry_image_4)
    modifieTelephoneEtudiantInput = Entry(master=editWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    modifieTelephoneEtudiantInput.place(x=35.0,y=288.0,width=260.0,height=21.0)
    editCanvas.create_text(35.0,275.0,anchor="nw",text="Téléphone",fill="#000000",font=("Inter", 11 * -1))
    modifieTelephoneEtudiantInput.insert(0,telephone)

    #input de modification de email
    image_image_8 = PhotoImage(master=editWindow, file=editWindowAssets("image_8.png"))
    editCanvas.create_image(457.0,294.0,image=image_image_8)
    entry_image_5 = PhotoImage(master=editWindow, file=editWindowAssets("entry_5.png"))
    editCanvas.create_image(456.0,299.5,image=entry_image_5)
    modifieEmailEtudiantInput= Entry(master=editWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    modifieEmailEtudiantInput.place(x=326.0,y=288.0,width=260.0,height=21.0)
    editCanvas.create_text(326.0,275.0,anchor="nw",text="Email",fill="#000000",font=("Inter", 11 * -1))
    modifieEmailEtudiantInput.insert(0,email)
    
    #input modification addresse
    image_image_9 = PhotoImage(master=editWindow, file=editWindowAssets("image_9.png"))
    editCanvas.create_image(311.0, 358.0, image=image_image_9)
    entry_image_6 = PhotoImage(master=editWindow, file=editWindowAssets("entry_6.png"))
    editCanvas.create_image(310.5, 363.5, image=entry_image_6)
    modifieAddresseEtudiantInput = Entry(master=editWindow, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    modifieAddresseEtudiantInput.place(x=35.0, y=352.0, width=551.0, height=21.0)
    editCanvas.create_text(35.0,339.0,anchor="nw",text="editress",fill="#000000",font=("Inter", 11 * -1))
    modifieAddresseEtudiantInput.insert(0,addresse)

    image_image_10 = PhotoImage(master=editWindow, file=editWindowAssets("image_10.png"))
    editCanvas.create_image(166.0, 167.0, image=image_image_10)

    setPreviewPic(f"./assets/uploaded/{resultat[1]}")

    button_image_2 = PhotoImage(master=editWindow, file=editWindowAssets("button_2.png"))
    selectImageBtn = Button(master=editWindow, image=button_image_2, borderwidth=0, highlightthickness=0, command=selectPic, relief="flat")
    selectImageBtn.place(x=196.0, y=215.0, width=96.0, height=25.0)

    button_image_3 = PhotoImage(master=editWindow, file=editWindowAssets("button_3.png"))
    submitBtn = Button(master=editWindow, image=button_image_3, borderwidth=0, highlightthickness=0, command=modifierEtudiant, relief="flat")
    submitBtn.place(x=28.0, y=402.0, width=96.0, height=25.0)

    button_image_4 = PhotoImage(master=editWindow, file=editWindowAssets("button_4.png"))
    cancelBtn = Button(master=editWindow, image=button_image_4, borderwidth=0, highlightthickness=0,command=lambda: closeWindow(editWindow), relief="flat")
    cancelBtn.place(x=137.0, y=402.0, width=96.0, height=25.0)

    editWindow.resizable(False, False)
    editWindow.mainloop()

def renderViewWindow(selectionDonneeEtudiant):
    
    matricule=selectionDonneeEtudiant[0]
    nom=selectionDonneeEtudiant[1]
    postnom=selectionDonneeEtudiant[2]
    telephone=selectionDonneeEtudiant[3]
    email=selectionDonneeEtudiant[4]
    addresse=selectionDonneeEtudiant[5]

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM etudiants WHERE matricule='{matricule}' ")
    resultat = cursor.fetchone()
    conn.commit()
    conn.close()

    print('Rendu de la fenêtre de visualisation des données')
    viewWindow = Tk()
    viewWindow.title('Fenêtre de visualisation Etudiant- Système de gestion des profiles des étudiants')
    viewWindow.geometry("720x480")
    viewWindow.configure(bg = "#FFFFFF")
    viewCanvas = Canvas(viewWindow,bg = "#FFFFFF",height = 480,width = 720,bd = 0,highlightthickness = 0,relief = "ridge")
    viewCanvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_1.png"))
    viewCanvas.create_image(360.0, 264.0, image=image_image_1)
    image_image_2 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_2.png"))
    viewCanvas.create_image(360.0, 24.0, image=image_image_2)
    viewCanvas.create_text(49.0, 10.0, anchor="nw", text="Visualiser l'Etudiant", fill="#FFFFFF", font=("Inter SemiBold", 24 * -1))
    image_image_3 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_3.png"))
    viewCanvas.create_image(28.0, 24.0, image=image_image_3)

    #input matricule
    image_image_5 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_5.png"))
    viewCanvas.create_image(456.0, 104.0, image=image_image_5)
    entry_image_2 = PhotoImage(master=viewWindow, file=viewWindowAssets("entry_2.png"))
    viewCanvas.create_image(455.0, 109.5, image=entry_image_2)
    matriculeInput = Entry(master=viewWindow, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    matriculeInput.place(x=325.0, y=98.0, width=260.0, height=21.0)
    matriculeInput.bind("<Key>", lambda e: "break")
    viewCanvas.create_text(325.0, 85.0, anchor="nw", text="Matricule", fill="#000000", font=("Inter", 11 * -1))
    matriculeInput.insert(0,matricule)

    #input nom
    image_image_4 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_4.png"))
    viewCanvas.create_image(457.0, 166.0, image=image_image_4)
    entry_image_1 = PhotoImage(master=viewWindow, file=viewWindowAssets("entry_1.png"))
    viewCanvas.create_image(456.0, 171.5, image=entry_image_1)
    nomInput = Entry(master=viewWindow,bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    nomInput.place(x=326.0, y=160.0, width=260.0, height=21.0)
    nomInput.bind("<Key>", lambda e: "break")
    viewCanvas.create_text(326.0, 147.0, anchor="nw", text="Nom", fill="#000000", font=("Inter", 11 * -1))
    nomInput.insert(0,nom)

    #input postnom
    image_image_6 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_6.png"))
    viewCanvas.create_image(457.0,230.0,image=image_image_6)
    entry_image_3 = PhotoImage(master=viewWindow, file=viewWindowAssets("entry_3.png"))
    viewCanvas.create_image(456.0,235.5,image=entry_image_3)
    postnomInput = Entry(master=viewWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    postnomInput.place(x=326.0,y=224.0,width=260.0,height=21.0)
    postnomInput.bind("<Key>", lambda e: "break")
    viewCanvas.create_text(326.0,211.0,anchor="nw",text="Post Nom",fill="#000000",font=("Inter", 11 * -1))
    postnomInput.insert(0,postnom)

    #input telephone
    image_image_7 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_7.png"))
    viewCanvas.create_image(166.0,294.0,image=image_image_7)
    entry_image_4 = PhotoImage(master=viewWindow, file=viewWindowAssets("entry_4.png"))
    viewCanvas.create_image(165.0,299.5,image=entry_image_4)
    telephoneInput = Entry(master=viewWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    telephoneInput.place(x=35.0,y=288.0,width=260.0,height=21.0)
    telephoneInput.bind("<Key>", lambda e: "break")
    viewCanvas.create_text(35.0,275.0,anchor="nw",text="Téléphone",fill="#000000",font=("Inter", 11 * -1))
    telephoneInput.insert(0,telephone)

    #input email
    image_image_8 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_8.png"))
    viewCanvas.create_image(457.0,294.0,image=image_image_8)
    entry_image_5 = PhotoImage(master=viewWindow, file=viewWindowAssets("entry_5.png"))
    viewCanvas.create_image(456.0,299.5,image=entry_image_5)
    emailInput = Entry(master=viewWindow, bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
    emailInput.place(x=326.0,y=288.0,width=260.0,height=21.0)
    emailInput.bind("<Key>", lambda e: "break")
    viewCanvas.create_text(326.0,275.0,anchor="nw",text="Email",fill="#000000",font=("Inter", 11 * -1))
    emailInput.insert(0,email)
    
    #input addresse
    image_image_9 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_9.png"))
    viewCanvas.create_image(311.0, 358.0, image=image_image_9)
    entry_image_6 = PhotoImage(master=viewWindow, file=viewWindowAssets("entry_6.png"))
    viewCanvas.create_image(310.5, 363.5, image=entry_image_6)
    addresseInput = Entry(master=viewWindow, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
    addresseInput.place(x=35.0, y=352.0, width=551.0, height=21.0)
    addresseInput.bind("<Key>", lambda e: "break")
    viewCanvas.create_text(35.0,339.0,anchor="nw",text="Addresse",fill="#000000",font=("Inter", 11 * -1))
    addresseInput.insert(0,addresse)

    image_image_10 = PhotoImage(master=viewWindow, file=viewWindowAssets("image_10.png"))
    viewCanvas.create_image(166.0, 167.0, image=image_image_10)
    image_image_11 = PhotoImage(master=viewWindow, file=f"./assets/uploaded/{resultat[1]}")
    viewCanvas.create_image(168.0, 168.0, image=image_image_11)

    viewWindow.resizable(False, False)
    viewWindow.mainloop()

mainWindow = Tk()
mainWindow.title('Accueil - Système de gestion des profiles des Etudiants')
mainWindow.geometry("1080x720")
mainWindow.configure(bg = "#FFFFFF")
mainCanvas = Canvas(mainWindow,bg = "#FFFFFF",height = 720,width = 1080,bd = 0,highlightthickness = 0,relief = "ridge")
mainCanvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(file=mainWindowAssets("image_1.png"))
image_1 = mainCanvas.create_image(645.0,397.0,image=image_image_1)
image_image_2 = PhotoImage(file=mainWindowAssets("image_2.png"))
image_2 = mainCanvas.create_image(648.0,398.0,image=image_image_2)
image_image_3 = PhotoImage(file=mainWindowAssets("image_3.png"))
image_3 = mainCanvas.create_image(540.0,37.0,image=image_image_3)
mainCanvas.create_text(73.0,15.0,anchor="nw",text="Système de Gestion des Profiles des Etudiants",fill="#FFFFFF",font=("Inter SemiBold", 36 * -1))
image_image_4 = PhotoImage(file=mainWindowAssets("image_4.png"))
image_4 = mainCanvas.create_image(38.0,36.0,image=image_image_4)
image_image_5 = PhotoImage(file=mainWindowAssets("image_5.png"))
image_5 = mainCanvas.create_image(105.0,397.0,image=image_image_5)

button_image_1 = PhotoImage(file=mainWindowAssets("button_1.png"))
button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=renderAddWindow,relief="flat")
button_1.place(x=28.0,y=105.0,width=148.0,height=57.0)

button_image_2 = PhotoImage(file=mainWindowAssets("button_2.png"))
button_2 = Button(image=button_image_2,borderwidth=0,highlightthickness=0,command=modifierEtudiant,relief="flat")
button_2.place(x=28.0,y=187.0,width=148.0,height=57.0)

button_image_3 = PhotoImage(file=mainWindowAssets("button_3.png"))
button_3 = Button(image=button_image_3,borderwidth=0,highlightthickness=0,command=supprimerEtudiant,relief="flat")
button_3.place(x=28.0,y=269.0,width=148.0,height=57.0)

button_image_4 = PhotoImage(file=mainWindowAssets("button_4.png"))
button_4 = Button(image=button_image_4,borderwidth=0,highlightthickness=0,command=voirEtudiant,relief="flat")
button_4.place(x=28.0,y=351.0,width=148.0,height=57.0)

button_image_5 = PhotoImage(file=mainWindowAssets("button_5.png"))
button_5 = Button(image=button_image_5,borderwidth=0,highlightthickness=0,command=exporterExcel,relief="flat")
button_5.place(x=28.0,y=433.0,width=148.0,height=57.0)

style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Inter SemiBold', 12),rowheight=30) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Inter SemiBold', 12,'bold'),background="black",foreground='black')
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

renderTreeVIew(LireLesDonneesDeLaBDD())

mainWindow.resizable(False, False)
mainWindow.mainloop()
