import numpy as np
import pandas as pd
import cmath
import matplotlib.pyplot as plt

U0 = 11 + 0j 
MAX_GRESKA = 0.0000001
NOVA_ITERACIJA = True
#print(type(U0))
# U je matrica napona svih 32 cvora, osim nultog
U = np.ones((32,1), dtype = complex)*11
#print(U)
iteracija = 0
max_iter = 100

I = np.zeros((32,1), dtype = complex) #I je matrica struja potrosnje koju treba da popunimo kroz racun
J = np.zeros((32,1), dtype = complex) #J je matrica struja po grani koju treba da popunimo kroz racun
JZ = np.ones((32,1), dtype = complex) #JZ je matrica gubitaka po grani koju treba da popunimo kroz racun
Z = np.ones((32,1), dtype = complex) #Z je matrica impedanse grana koju treba da popunimo kroz racun
Ustaro = np.ones((32,1), dtype = complex) #Ustaro je matrica prethodnih vrednosti napona cvorova
G = np.ones((32,1), dtype = complex) #G je matrica razlike apsolutnih vrednosti starog i novog napona cvora
Br_cvora = np.empty((32,1)) #Redni broj cvora je matrica koju koristim za laksi prikaz grafika
Br_grane = np.empty((32,1)) #Redni broj grane je matrica koju koristim za laksi prikaz grafika
#print(J)

#Ubacio sam iz excela podatke o snagama potrosnje po cvoru
Snage_po_cvorovima = pd.read_csv("Potrosnja-i-proizvodnja-snage-po-cvorovima.csv")
Snage_po_cvorovima = np.matrix(Snage_po_cvorovima)
#print(Snage_po_cvorovima)

# Ubacio sam iz excela parametre i graf mreze
Graf_i_parametri = pd.read_csv("Graf-kola-parametri-i-nivo-mreze.csv")
Graf_i_parametri = np.matrix(Graf_i_parametri)
#print(Graf_i_parametri)

#formiranje prazne matrice kompleksnih snaga potrosnje po cvoru
Sdk = np.empty((32,1), dtype = complex)

"""VEZBA: Ubacivanje elementa po element u matricu kompleksnih brojeva
Prazna_matrica = np.empty((3,4), dtype = complex)

for i in range (3):
	for j in range(4):
		Prazna_matrica[i,j] = i

print(Prazna_matrica)
"""


# Popunjavanje matrice snage potrosnje u svakom cvoru:

for i in range(32):
	#local A, B
	A = Snage_po_cvorovima[i,1] - Snage_po_cvorovima[i,3]
	B = (Snage_po_cvorovima[i,2] - Snage_po_cvorovima[i,4])*1j 
	Sdk[i,0] = A + B
#print(Sdk)
#print(Sdk[10,0])

# Kraj popunjavanja matrice snage potrosnje u svakom cvoru.

# Matrica impedanse grana:

for i in range(32):
	Z[i] = Graf_i_parametri[i,3] + Graf_i_parametri[i,4]*1j

#print(Z)
# Kraj popunjavanja matrice impedansi



while NOVA_ITERACIJA:

	# Popunjavanje matrice struje potrosnje u svakom cvoru:
	for i in range(32):
		A = Sdk[i]/U[i]
		I[i,0] = np.conjugate(A)
		
	#print(I)

	# Kraj popunjavanja matrice struje potrosnje.




	# Proracun struje po granama:
	for j in range(17,0,-1):
		for i in range (32):
			if Graf_i_parametri[i,5] == j:
				A = 0+0j
				Zavrsni_cvor = int(Graf_i_parametri[i,2])
				Broj_grane = int(Graf_i_parametri[i,0])
				for k in range(32):
					if Graf_i_parametri[k,1] == Zavrsni_cvor:
						A += J[k,0] 
				J[Broj_grane-1,0] = I[Zavrsni_cvor-1,0] + A

	#print((I[0,0])+J[1,0]+J[28,0])
	#print(J[0,0])
	#print(I[20,0])
	#print("")
	#print(J)

	# Kraj proracuna struja po granama.


	#Popunjavanje matrice gubitaka JZ:

	for i in range(32):
		JZ[i] = Z[i]*J[i]

	#print("")
	#print(JZ)
	# Kraj popunjavanja matrice gubitaka JZ.

	# Racunanje napona cvorova:
	for i in range (32):
		Ustaro[i] = U[i]  
	#print(Ustaro)

	U[0,0] = U0 - JZ[0,0]
	#print(U[0,0])

	for k in range (2,18):
		for i in range(32):
			if Graf_i_parametri[i,5] == k:
				Zcv = int(Graf_i_parametri[i,2])
				Pcv = int(Graf_i_parametri[i,1])
				Grana = int(Graf_i_parametri[i,0])
				U[Zcv-1, 0] = U[Pcv-1, 0] - JZ[Grana-1, 0]

	#print("")
	#print(U)
	#print("")
	#print(abs(U))
	#print(Ustaro)

	for i in range (32):
		G[i] = Ustaro[i] - U[i]

	#print(G)
	#print(" APS")
	#print(abs(G))
	#print("")
	Max = (max(abs(G)))
	iteracija += 1
	print("Iteracija: " + str(iteracija))
	print("Maksimalna greska = " + str(Max))
	if (Max < MAX_GRESKA):
		break
	if iteracija == max_iter:
		break


if iteracija == max_iter:
	print("Iterativni postupak divergira!")
else:
	#print("")
	#print(Max)
	print("")
	print("APSOLUTNA OD U")
	print(abs(U))
	print("")
	print("Apsolutna od J")
	print(abs(J))
		




for i in range (32):
	Br_cvora[i,0] = Snage_po_cvorovima[i,0]
	Br_grane[i,0] = Graf_i_parametri[i,0]

#print(Br_cvora) 
plt.plot(Br_cvora,abs(U), marker = "o")
plt.title ("Grafik napona po cvorovima")
plt.xlabel("Redni broj cvora")
plt.ylabel("Napon [kV]")
plt.show()
plt.close()


plt.plot(Br_grane,abs(J), marker = "o")
plt.title ("Grafik struja po granama")
plt.xlabel("Redni broj cvora")
plt.ylabel("Struja [kA]")
plt.show()
plt.close()

#plt.plot(Br_cvora,U)
#plt.show()
#plt.close()

print("Struja J1:")
print(J[0,0])
print("")
print("Struja J2:")
print(J[1,0])
