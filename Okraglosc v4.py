


import geopandas as gpd
import pandas as pd 
import matplotlib.pyplot as plt 
#import geoplot
my_path = 'D:\\KK\\OneDrive\\Wroclaw w Liczbach\\Gotowe projekty\\\\20201031 Okrągłość\\'


INPUT_FILE = 'D:\\KK\\OneDrive\\Wroclaw w Liczbach\\Granice\\OKWSejm\\OKW.shp'
NAZWA = 'OKW'
FOLDER = 'OKW Sejm\\'
#senat
INPUT_FILE = 'D:\\KK\\OneDrive\\Wroclaw w Liczbach\\Granice\\OKWSenat\\senat_2019.shp'
NAZWA = 'nr_ok'
FOLDER = 'OKW Senat\\'
#powiaty
INPUT_FILE = 'D:\\KK\\OneDrive\\Wroclaw w Liczbach\\Granice\\Powiaty\\Powiaty.shp'
NAZWA = 'JPT_NAZWA_'
FOLDER = ''


Granice_Powitów = gpd.read_file(INPUT_FILE, encoding="utf-8") #.loc[[0],'geometry']
#Granice_Powitów.geometry.centroid.x
#Granice_Powitów.plot()


ECKERT_IV_PROJ4_STRING = "+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
Granice_Powitów_proj = Granice_Powitów.to_crs(ECKERT_IV_PROJ4_STRING)

okraglosci = pd.DataFrame()
promienie  = pd.DataFrame()
for index, row in Granice_Powitów_proj.iterrows():
    powiat = row[NAZWA]
    print(str(powiat) + ' - ' + str(index) + ' z ' + str(len(Granice_Powitów_proj.index)))
    Granice_Powitów_proj_wybrane = Granice_Powitów_proj.iloc[[index]] 
    
    roznica = 1
    promien = 0.1
    while roznica > 0:
        #print(round(roznica))
        roznica = Granice_Powitów_proj_wybrane.difference(Granice_Powitów_proj_wybrane.geometry.centroid.buffer(promien * 1000)).area
        roznica = roznica.reset_index(drop = True)[0]
        promien = promien + 0.1

    powierzchnia_miasta = Granice_Powitów_proj_wybrane.area
    powierzchnia_okregu = Granice_Powitów_proj_wybrane.geometry.centroid.buffer(promien * 1000).area

    procent = (powierzchnia_miasta / powierzchnia_okregu).reset_index(drop = True)[0]
    
    okraglosci = okraglosci.append(pd.DataFrame({'o': [procent]}, index = [0])) 
    promienie  = promienie.append(pd.DataFrame({'promien': [promien]}, index = [0]))
    #wykres
    okrag = Granice_Powitów_proj_wybrane.geometry.centroid.buffer(promien * 1000).boundary.plot()
    Granice_Powitów_proj_wybrane.plot(ax = okrag, alpha = 0.5)
    #osie    
    plt.axis('off')
    plt.title(str(powiat) + '\n' + 'Okrągłość: ' + str(round(procent * 100, 1)) + '%')
    #zapis
    plt.savefig(my_path + FOLDER + '\\Wykresy\\' + str(powiat) + ' - ' + str(round(procent * 100)) + '.png')
    #zamknij
    plt.close()
    plt.clf()
    
    

print('dodaie kolumn')
Granice_Powitów_proj['promien']   = promienie.iloc[:, 0].reset_index(drop = True)
Granice_Powitów_proj['okraglosc'] = okraglosci.iloc[:, 0].reset_index(drop = True)



#zapis wynikow
Granice_Powitów_proj.to_file(my_path + FOLDER + "Wynik.shp")
Granice_Powitów_proj.to_file(my_path + FOLDER + "Wynik.gpkg", layer='countries', driver="GPKG")
#wczytanie
#Granice_Powitów_proj = gpd.read_file(my_path + "\\Wynik.shp", encoding="utf-8") #.loc[[0],'geometry']


Granice_Powitów_proj_sort = Granice_Powitów_proj.sort_values(by = 'okraglosc', ascending = False).reset_index(drop = True)
#Granice_Powitów_proj_sort = Granice_Powitów_proj_sort.loc[[0, 1, 2, 376, 378, 379], ['JPT_NAZWA_', 'okraglosc', 'promien', 'geometry']]
Granice_Powitów_proj_sort = Granice_Powitów_proj_sort.loc[[0, 1, 2, 97, 98, 99], [NAZWA, 'okraglosc', 'promien', 'geometry']]
 



fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows = 3, ncols = 2, 
     sharex = False, sharey = False, constrained_layout = True)

#fig.suptitle('This is a somewhat long figure title', fontsize=16)
#fig.suptitle("Najbardziej i najmniej okrągłe powiaty w Polsce", fontsize=16)
fig.suptitle("Najbardziej i najmniej okrągłe okredi wyborcze do senatu w Polsce", fontsize=16)
#ax 1
i = 0
Granice_Powitów_proj_sort.iloc[[i]].plot(ax = ax1, alpha = 0.5)
Granice_Powitów_proj_sort.iloc[[i]].geometry.centroid.buffer(Granice_Powitów_proj_sort.iloc[i].promien * 1000).boundary.plot(ax = ax1)
ax1.title.set_text(str(Granice_Powitów_proj_sort.iloc[i][NAZWA]) + '\n' + 'Okrągłość: ' + str(round(Granice_Powitów_proj_sort.iloc[i].okraglosc * 100, 1)) + '%')
ax1.axis('off')
#ax 3
i = 1
Granice_Powitów_proj_sort.iloc[[i]].plot(ax = ax3, alpha = 0.5)
Granice_Powitów_proj_sort.iloc[[i]].geometry.centroid.buffer(Granice_Powitów_proj_sort.iloc[i].promien * 1000).boundary.plot(ax = ax3)
ax3.title.set_text(str(Granice_Powitów_proj_sort.iloc[i][NAZWA]) + '\n' + 'Okrągłość: ' + str(round(Granice_Powitów_proj_sort.iloc[i].okraglosc * 100, 1)) + '%')
ax3.axis('off')
#ax 5
i = 2
Granice_Powitów_proj_sort.iloc[[i]].plot(ax = ax5, alpha = 0.5)
Granice_Powitów_proj_sort.iloc[[i]].geometry.centroid.buffer(Granice_Powitów_proj_sort.iloc[i].promien * 1000).boundary.plot(ax = ax5)
ax5.title.set_text(str(Granice_Powitów_proj_sort.iloc[i][NAZWA]) + '\n' + 'Okrągłość: ' + str(round(Granice_Powitów_proj_sort.iloc[i].okraglosc * 100, 1)) + '%')
ax5.axis('off')

#ax 2
i = 5
Granice_Powitów_proj_sort.iloc[[i]].plot(ax = ax2, alpha = 0.5)
Granice_Powitów_proj_sort.iloc[[i]].geometry.centroid.buffer(Granice_Powitów_proj_sort.iloc[i].promien * 1000).boundary.plot(ax = ax2)
ax2.title.set_text(str(Granice_Powitów_proj_sort.iloc[i][NAZWA]) + '\n' + 'Okrągłość: ' + str(round(Granice_Powitów_proj_sort.iloc[i].okraglosc * 100, 1)) + '%')
ax2.axis('off')
#ax 4
i = 4
Granice_Powitów_proj_sort.iloc[[i]].plot(ax = ax4, alpha = 0.5)
Granice_Powitów_proj_sort.iloc[[i]].geometry.centroid.buffer(Granice_Powitów_proj_sort.iloc[i].promien * 1000).boundary.plot(ax = ax4)
ax4.title.set_text(str(Granice_Powitów_proj_sort.iloc[i][NAZWA]) + '\n' + 'Okrągłość: ' + str(round(Granice_Powitów_proj_sort.iloc[i].okraglosc * 100, 1)) + '%')
ax4.axis('off')
#ax 6
i = 3
Granice_Powitów_proj_sort.iloc[[i]].plot(ax = ax6, alpha = 0.5)
Granice_Powitów_proj_sort.iloc[[i]].geometry.centroid.buffer(Granice_Powitów_proj_sort.iloc[i].promien * 1000).boundary.plot(ax = ax6)
ax6.title.set_text(str(Granice_Powitów_proj_sort.iloc[i][NAZWA]) + '\n' + 'Okrągłość: ' + str(round(Granice_Powitów_proj_sort.iloc[i].okraglosc * 100, 1)) + '%')
ax6.axis('off')

#zapis
plt.savefig(my_path + '\\Wykresy\\' + FOLDER + 'Podsumowanie' + '.png')
#zamknij
plt.close()
plt.clf()



