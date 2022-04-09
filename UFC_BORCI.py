class Borec:
    def __init__(self,ime,starost,višina, MMAR, kategorija,nickname):
        '''ustvari borca'''
        i = MMAR.find(' ')
        if i >= 0:
            MMAR = MMAR[:i]
            
        self.ime = ime
       
        if 21 <= int(starost) < 26:
            starost = [1, str(starost)]
        elif 26 <= int(starost) < 30:
            starost = [2, str(starost)]
        elif 30 <= int(starost) < 35:
            starost = [3, str(starost)]
        elif 35 <= int(starost) < 40:
            starost = [4, str(starost)]
        elif 40 <= int(starost) < 45:
            starost = [5, str(starost)]
        self.starost = starost
       
        višina = float(višina[-7:-3])
        
        
        
        self.višina = višina
        
        
        self.MMAR = MMAR.split('–')
         
        if kategorija == 'FLW':
            kategorija = [5,'Flyweight']
        elif kategorija == 'BW':
            kategorija = [10,'Bantamweight']
        elif kategorija == 'FW':
            kategorija = [15,'Featherweight']
        elif kategorija == 'LW':
            kategorija = [20,'Lightweight']
        elif kategorija == 'WW':
            kategorija = [25,'Welterweight']
        elif kategorija == 'MW':
            kategorija = [30,'Middleweight']
        elif kategorija == 'LHW':
            kategorija = [35,'Light heavyweight']
        elif kategorija == 'HW':
            kategorija = [40,'Heavyweight']

        self.kategorija = kategorija
        self.nickname = nickname
   
    def __str__(self):
        return self.ime+' '+self.starost+' '+self.višina+' '+self.MMAR+' '+self.kategorija+' '+self.nickname
    def __repr__(self):
        return 'Borec({}, {}, {}, {}, {}, {})'.format(repr(self.ime),repr(self.starost),repr(self.višina),repr(self.MMAR),repr(self.kategorija),repr(self.nickname))
   
   
   
   
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import numpy as np







def Podatki_Borca(iskani_borec):
    ''' Funkcija vrne statistiko danih borcev'''
   
   
    vsi_borci = []
    teznost = ['HW','LHW','MW','WW','LW','FW','BW','FLW']
    url_LE = "https://en.wikipedia.org/wiki/List_of_current_UFC_fighters"
    response = requests.get(url_LE)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('div', class_='vector-body')
    data = body.find('div', class_='mw-body-content mw-content-ltr')
    tabele = data.find_all('table')

    for indeks in range(len(teznost)):
       
        k = 9 + indeks
        tab = tabele[k]
        borci = []

        for vrstica in tab.find_all('tr'):
            podatki = []
            for el_vrstice in vrstica.find_all('td'):
                podatki.append(el_vrstice.text.strip().replace('\xa0',' '))
            if len(podatki) > 8:
               
                vsi_borci.append(Borec(podatki[1],podatki[2],podatki[3],podatki[8],teznost[indeks],podatki[4]))
       
    for borec in vsi_borci:
        if iskani_borec in borec.ime:
            return borec


def Napovedovalec_Zmagovalca_Ter_Prikaz_Statistik(prvi_borec, drugi_borec):
    ''' Funkcija sprejme dva borca, ter glede na njune preddoločene statistike proba ugotoviti kdo bi zmagal v boju in vrne zmagovalca'''
    
    prvi = Podatki_Borca(prvi_borec)
    drugi = Podatki_Borca(drugi_borec)
    score_prvi = (int(prvi.MMAR[0])- int(prvi.MMAR[1]))
    score_drugi = (int(drugi.MMAR[0])-  int(drugi.MMAR[1]))
    točke_prvega_borca =  0.6*score_prvi + prvi.starost[0] + prvi.kategorija[0]
    točke_drugega_borca =  0.6*score_drugi + drugi.starost[0] + drugi.kategorija[0]
   
    if prvi.višina > drugi.višina:
        točke_prvega_borca += 5
    else:
        točke_drugega_borca += 5
       
    print('Get ready for ' + prvi.ime + ' Versus ' + drugi.ime + ' !\n')
    print('     Category: ' + prvi.kategorija[1] +' vs '+ drugi.kategorija[1])
    print('     Height: ' + str(prvi.višina) + ' m' +' vs '+ str(drugi.višina) + ' m')
    print('     Age: ' + str(prvi.starost[1]) + ' years' +' vs '+ str(drugi.starost[1]) + ' years')
    print('     MMA Record: ' + str(prvi.MMAR[0]) +'-'+str(prvi.MMAR[1]) +' vs '+ str(drugi.MMAR[0])+'-'+str(drugi.MMAR[1])+'\n' )
    
    
    
    if točke_prvega_borca > točke_drugega_borca:
        if prvi. nickname is not '':
            print ("And the WINNER is " + prvi.ime +' also known as ' + prvi.nickname + ' !')
        else:
            print ("And the WINNER is " + prvi.ime + ' !')
            
    else:
        if prvi. nickname is not '':
            print ("And the WINNER is " + drugi.ime +' also known as ' + drugi.nickname + ' !')
        else:
            print ("And the WINNER is " + drugi.ime + ' !')
            
    X = ['Kategorija','Višina','Starost','MMAR Rekord']
    y = [prvi.kategorija[0], prvi.višina*18, int(prvi.starost[1])*0.8, score_prvi]
    z = [drugi.kategorija[0], drugi.višina*18, int(drugi.starost[1])*0.8, score_drugi]
      
    X_axis = np.arange(len(X))
      
    plt.bar(X_axis - 0.2, y, 0.4, label = str(prvi.ime))
    plt.bar(X_axis + 0.2, z, 0.4, label = str(drugi.ime))
      
    plt.xticks(X_axis, X)
    plt.legend()
    plt.show()
            
            
Testni_vzorec = Napovedovalec_Zmagovalca_Ter_Prikaz_Statistik('Conor McGregor', 'Alexander Gustafsson')