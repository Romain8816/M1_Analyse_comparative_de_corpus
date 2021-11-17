import tkinter as tk
from tkinter import ttk
from analyse_comparative import data_cleaning,get_reddit
from interface_classes import valider_tab3,valider_tab2,Checkbox,available_themes
import classes
import os


directory=os.getcwd()

# FENETRE PRINCIPAL
root = tk.Tk()
root.title("Projet")

# postionnement de la fenêtre
screen_x = int(root.winfo_screenwidth()) # largeur de l'écran
screen_y = int(root.winfo_screenheight()) # hauteur de l'écran
window_x = 1000 # largeur de la fenêtre
window_y = 550 # hauteur de la fenêtre
posX = (screen_x//2)-(window_x //2) # position de la largeur de la fenêtre
posY = (screen_y //2)-(window_y//2) # position de la hauteur de la fenêtre
geo = "{}x{}+{}+{}".format(window_x,window_y,posX, posY)
root.geometry(geo)
#root.resizable(width=False,height=False) # Non redimensionable



############### CREATION NOTEBOOK (conteneur à onglets)
tabControl = ttk.Notebook(root)

# créations des onglets et ajout au notebook
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='Thématiques à télécharger')
tabControl.add(tab1, text='Analyse comparative de corpus')
tabControl.add(tab2, text='Evolution temporelle d\'un mot')
tabControl.pack(fill="both") # Positionnement des onglets 




############## TAB3: TELECHARGEMENT DES DOCUMENTS

tab3_frame1 = tk.LabelFrame(tab3,padx=5,pady=5,borderwidth=0)
tab3_frame2 = tk.LabelFrame(tab3,padx=200,pady=30,borderwidth=0)
tab3_frame1.grid(row=0,column=0)
tab3_frame2.grid(row=0,column=1)


tab3_choix = tk.Label(tab3_frame1,text="Sélectionner les corpus à télécharger pour les thèmes suivants :")
tab3_src = tk.Label(tab3_frame2,text="Sélectionner les sources à utiliser :")
tab3_choix.grid(row=0,column=0,padx=5)
tab3_src.grid(row=0,sticky='nw',padx=5)

#Ajout des checkbutton sur les thèmes
tab3_frame1_ckb1=Checkbox('Coronavirus',tab3_frame1,1)
tab3_frame1_ckb2=Checkbox('Energie nucléaire',tab3_frame1,1)
tab3_frame1_ckb1.chk.grid(row=1,sticky='nw',padx=8)
tab3_frame1_ckb2.chk.grid(row=2,sticky='nw',padx=8)

#liste des themes
ckb_themes_list = [tab3_frame1_ckb1,tab3_frame1_ckb2]

# Ajout des checkbutton sur les sources
tab3_frame2_ckb1=Checkbox('Reddit',tab3_frame2,1)
tab3_frame2_ckb2=Checkbox('Arxiv',tab3_frame2,1)
tab3_frame2_ckb1.chk.grid(row=1,sticky='nw',padx=8)
tab3_frame2_ckb2.chk.grid(row=2,sticky='nw',padx=8)

# liste des sources
ckb_source_list = [tab3_frame2_ckb1,tab3_frame2_ckb2]

# bouton de validation
button = tk.Button(tab3,text="VALIDER",command=lambda: valider_tab3(ckb_themes_list,ckb_source_list))
button.grid(row=2,sticky='nw',padx=8)

############## TAB1 : ANALYSE DE CORPUS

# Liste des choix de thèmes et des sources : 
themes=[] # modifiés dans la fonction available_themes
sources = ['Reddit','Arxiv']

# création de sous frames
tab1_frame1 = tk.LabelFrame(tab1,padx=5,pady=5,borderwidth=0)
tab1_frame2 = tk.LabelFrame(tab1,padx=200,pady=30,borderwidth=0)
tab1_frame1.grid(row=0,column=0)
tab1_frame2.grid(row=0,column=1)


# Ajout des labels
tab1_theme = tk.Label(tab1_frame1,text="Thème :")
fill_space = tk.Label(tab1_frame1,text=" ")
tab1_theme.grid(row=0,column=0,padx=5)
fill_space.grid(row=1,column=0,padx=5)

tab1_source1 = tk.Label(tab1_frame2,text="Source 1 :")
tab1_source2 = tk.Label(tab1_frame2,text="Source 2 :")
tab1_source1.grid(row=1)
tab1_source2.grid(row=2)


# Ajout des combobox
tab1_cbxTheme = ttk.Combobox(tab1_frame1,values = themes,postcommand=lambda: available_themes(directory,tab1_cbxTheme))
tab1_cbxSource1 = ttk.Combobox(tab1_frame2,values = sources)
tab1_cbxSource2 = ttk.Combobox(tab1_frame2,values = sources)

tab1_cbxTheme.grid(row=0,column=1,padx=8)
tab1_cbxSource1.grid(row=1,column=2,padx=8)
tab1_cbxSource2.grid(row=2,column=2,padx=8,pady=10)

tab1_button = tk.Button(tab1,text="VALIDER",command=lambda:valider_tab2(tab1_cbxTheme,tab1_cbxSource1,tab1_cbxSource2,directory))
tab1_button.grid(row=2,sticky='nw',padx=8)

############## TAB2 : EVOLUTION TEMPORELLE D'UN MOT

# Ajout des widgets à l'onglet de l'évolution temporelle des mots :
tab_frame2 = tk.LabelFrame(tab2,padx=5,pady=5,borderwidth=0)
tab2_choix = tk.Label(tab_frame2,text="Choix du thème :").grid(row=0,column=0)
tab2_button = tk.Button(tab2,text="VALIDER")
tab2_button.grid(row=2,sticky='nw',padx=8)  #N'a pas été implémenté



root.mainloop()