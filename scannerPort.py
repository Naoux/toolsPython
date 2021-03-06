import socket
import sys, os
import errno
from tqdm import tqdm

portOuvert = []
portFerme = []
PORT = []

if len(sys.argv) == 3 or len(sys.argv) == 4:
	try:
		HOST = sys.argv[1]
	except:
		print("[-] Domaine invalide")
		sys.exit()

	try:
		PORTmin = sys.argv[2]
	except:
		print("[-] Port invalide.")
		sys.exit()

	if len(sys.argv) == 4:
		try:
			PORTmax = int(sys.argv[3])
		except:
			print("[-] Port invalide")
			sys.exit()

	try:
		PORTmin = int(PORTmin)
		if len(sys.argv) == 4:
			for n in range(PORTmin, PORTmax + 1):
				PORT.append(n)
				n += 1
		else:
			PORT.append(PORTmin)
	except ValueError:
		print("[-] Port invalide")
		sys.exit()

	pbar = tqdm(total=len(PORT[:]))

	i = 0
	while i < len(PORT[:]):
		pbar.update(1)
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(1)
		except socket.error as e:
			print("[-] Une erreur est survenue lors de la creation du socket ! {}".format(e))
			sys.exit()

		try:
			scan = sock.connect_ex((HOST, PORT[i]))
			if scan == 0:
				sock.shutdown(socket.SHUT_RDWR)
				sock.close()
				portOuvert.append(PORT[i])
			else:
				if errno.errorcode[errno.ECONNREFUSED]:
					portFerme.append(PORT[i])
				else:
					print("[-] Hote introuvable")
					j = 1
					i = len(PORT[:])
			i += 1
		except socket.gaierror as e:
			print("[-] Erreur d'adresse de connexion au serveur: {}".format(e))
			sys.exit()
		except socket.error as e:
			print("[-] Erreur de connexion : {}".format(e))
			sys.exit()

	pbar.close()
	if "win" in sys.platform:
		try:
			os.system("cls")
		finally:
			pass
	else:
		try:
			os.system("clear")
		finally:
			pass

	with  open("scan.result", "w") as file:
		if len(portOuvert) == 0:
			print("[-] Tous les ports sont fermes !")
		else:
			for port in portOuvert:
				file.write("[+] Port {} ouvert\n".format(port))
			for port in portFerme:
				file.write("[-] Port {} ferme\n".format(port))

else:
	print("Usages: python scannerPort.py <domaine/ip> <PORT>\n",
	      "\tpython scannerPort.py <domaine/ip> <PORTmin> <PORTmax>")
