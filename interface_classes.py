# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from analyse_comparative import*
import os
import pickle
import operator

class Checkbox():
    def __init__(self,txt,frame=None,def_val=0):
        var2 = tk.IntVar()
        var2.set(def_val)
        
        self.txt=txt
        self.def_val=var2
        
        if frame==None:
            self.chk = ttk.Checkbutton(text=txt,var=self.def_val)
        else:
            self.chk = ttk.Checkbutton(frame,text=txt,var=self.def_val)
        
    def def_value(self):
        return self.def_val.get()
    
                

# Les thèmes peuvent être sélectionnés uniquement si ils ont été téléchargés (sauvegarder en .pickle)
def available_themes(directory,tab1_cbxTheme):
    themes=[]
    for filename in os.listdir(directory):
        if filename.endswith(".pickle"):
            themes.append(filename.split('.')[0])
        else:
            continue
    tab1_cbxTheme["values"] = themes


# fonction qui permet de valider les choix des thèmes et des sources
def valider_tab3(ckb_themes,ckb_sources):
    sum1=0
    sum2=0
    liste_themes=[]
    liste_sources=[]
    #global liste_corpus
    #liste_corpus = []
    corpus=[]
    
    
    for t in ckb_themes:
        if t.def_value()==1:
            sum1=sum1+1
            liste_themes.append(t.txt)
     #vérification que l'ensemble des checkbox requis sont cochés       
    for s in ckb_sources:
        if s.def_value()==1:
            sum2=sum2+1
            liste_sources.append(s.txt)
            
    if (sum1==0 or sum2==0):
        tk.messagebox.showerror("Erreur","Sélectionner au moins une source et un thème")
        
    else:
        for i in liste_themes:
            crp = Corpus(i)     #création d'une instance de la classe corpus
            docs=[]
            for j in liste_sources:
                if j =='Reddit':
                    # on ajoute dans la liste docs la liste de Documents() retournés par get_reddit
                    docs.append(get_reddit(i)) 
                elif j=='Arxiv':
                    # on ajoute dans la liste docs la liste de Documents() retournés par get_arxiv
                    docs.append(get_arxiv(i))
                crp.add_source(j)
                
            # on a la liste de liste : docs = [[],[]]
            for k in docs:
                for l in k:
                    crp.add_doc(l)
            crp.save(i+".pickle")
            #liste_corpus.append(corpus)
        tk.messagebox.showinfo("Info","Téléchargement terminé")
    #return available_themes

#permet de valider les choix fait dans les différents combobox de la fenetre 2 et lancer l'analyse comparative avec l'affichage des différents graphiques
def valider_tab2(cbx_theme,cbx_src1,cbx_src2,directory):
    theme=cbx_theme.get()
    src1=cbx_src1.get()
    src2=cbx_src2.get()
    src_list=[src1,src2]
    corpus_n1=[]
    corpus_n2=[]

    if not theme:
        tk.messagebox.showerror("Erreur","Aucun thème sélectionné ou téléchargé")
    elif src1==src2 or not src1 or not src2:
        tk.messagebox.showerror("Erreur","Source non sélectionnée ou sources identiques")
    else:
        with open(theme+'.pickle', 'rb') as f: 
            data = pickle.load(f) # Corpus
        download_source = data.get_sources()
        
        if (src1 or src2) not in download_source: 
           tk.messagebox.showerror("Erreur","veuillez télécharger le corpus en sélectionnant les sources à comparer")
        else :
            for key, value in data.collection.items():

                if src1 in value.get_source():
                    corpus_n1.append(value)
                elif src2 in value.get_source():
                    corpus_n2.append(value)
                    
        
            res=compare(corpus_n1,corpus_n2)
            bar_plot(res[0].split(' ')) #problème seul le premier barplot est affiché, tous ce qui se passe après cette ligne n'est pas exécutée,
            bar_plot(res[1].split(' ')) #nous n'avons pas trouvé la solution pour afficher tous les barplot, il faudra lors de la sélection de la source mettre Reddit en premier pour avoir le barplot concernant les mots de reddit et inversement pour arxiv
                             

    
    

    
    