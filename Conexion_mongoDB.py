import json
import random
from pymongo import MongoClient

#Connecting to a MongoDB database of AppleMusic songs
class PlaylistRepositorio:
    def __init__(self, cadena_conexion):
        cliente = MongoClient(cadena_conexion)
        self.db = cliente.get_database("playlistdb")
        self.db.playlist.create_index("nombre", unique =True)   
        #cliente.close()
            
    def insertar_canciones(self,lista_canciones):
        # songs_lists=[{nombre:str,cantante:str,genero:str,album:str,url:str},...]
        self.db.get_collection("canciones").insert_many(lista_canciones)
        
    def exist(self, nombre):
        diccionario = self.db.playlist.find_one({"nombre": nombre})
        return not diccionario is None       
            
    def insert(self,dicPlaylist):
        if dicPlaylist["nombre"] is None:
            raise "Es necesario el nombre de la playlist"
        playlist = {
                   "nombre":dicPlaylist["nombre"],
                   "username":dicPlaylist["username"],
                   "canciones":dicPlaylist["canciones"],
                   }
        result = self.db.playlist.insert_one(playlist)
        return result.inserted_id
        
    def update(self, varPlaylist):
        self.db.playlist.update_one({"nombre":{"$eq":varPlaylist["nombre"]}},{"$set":{"username":varPlaylist["username"],"canciones":varPlaylist["canciones"]}})
    
    def find(self,nombre):
        diccionario = self.db.playlist.find_one({"nombre": nombre})
        return diccionario
  
    def sugerencias(self,n,generos):
        cursor = self.db.canciones.aggregate([
            {"$match":{"genero":{"$in":list(generos)}}},
            {"$sample":{"size":n}}, 
            {"$group":{"_id":"$genero","count":{"$sum":1},"nombres":{"$push":"$nombre"}}},  
            {"$unwind":{"path":"$nombres"}},
            {"$project":{"_id":0,"nombres":1}},
        ])

        return list(doc["nombres"] for doc in cursor)
    
    def mostrar_canciones(self,nombre):
        cursor = self.db.playlist.aggregate([
            {"$match":{"nombre":nombre}},
            {"$unwind":{"path":"$canciones"}},
            {"$project":{"_id":0,"canciones":1}},
        ])
        return list(doc["canciones"] for doc in cursor)
    
    def consultar_playlists(self,nombre,nombre_usuario):
        cursor = self.db.playlist.aggregate([
            {"$match":{"nombre":{"$ne":nombre},"username":nombre_usuario}},
            {"$project":{"_id":0,"nombre":1}}
        ])
        return list(doc["nombre"] for doc in cursor)

repo = PlaylistRepositorio("mongodb://localhost:27017/")

class Playlist:
    
    def __init__(self,nombre,username,canciones=None):
        self.id = None
        self.nombre = nombre
        self.username = username
        self.canciones = canciones
    def __str__(self):
        return f"Nombre playlist: {self.nombre}, nombre usuario {self.username}, canciones: {self.canciones}"
        
    def guardar(self):
        if repo.exist(self.nombre):
            repo.update(vars(self))
        else:
            self.id = repo.insert(vars(self))        
       
    def recuperar(self):
        dic = repo.find(self.nombre)
        self.id = dic["_id"]
        self.username = dic["username"]
        self.canciones = dic["canciones"]
            
    def agregar_cancion(self,diccionario):
        if self.canciones is None:
            self.canciones = []
        self.canciones.append(diccionario)
        self.guardar()
            
    def obtener_sugerencias(self,n,lista):
        return repo.sugerencias(n,lista)
        #return repo.sugerencias(n,[(cancion["genero"] for cancion in self.canciones)])
    
def Enmarcar(begin,after):
    def Enmarcar_sub(funcion):
        def inner(self):
            print(begin)
            funcion(self)
            print(after)
        return inner
    return Enmarcar_sub
            
class PlaylistConsole(Playlist):
       
    def mostrar_sugerencias(self, n):
        print(self.obtener_sugerencias(n))

    @Enmarcar("*"*10,"*"*10)
    def mostrar_canciones(self):
        print(repo.mostrar_canciones(self.nombre).__str__())
    
    def consultar_playlists(self):
        print(f"Listas de este usuario: {repo.consultar_playlists(self.nombre,self.username)}")

def nuevo_playlistConsole():
    nombre = input("Introduzca el nombre de la playlist: ")
    usuario = input("Introduzaca el nombre de usuario: ")
    playlist = PlaylistConsole(nombre,usuario)
    return playlist