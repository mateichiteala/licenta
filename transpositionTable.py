import json
import random

from mongoengine import Document, IntField, FloatField, ListField, LongField
from mongoengine import connect, disconnect

from conn import database_info
from pieces.piece import Piece

class ZobristTable(Document):
    row = IntField(required=True, unique=True)
    cols = ListField(ListField(LongField()))


class HashTable(Document):
    hash = LongField(primary_key=True)
    score = FloatField(required=True)
    depth = IntField(required=True)

    
class TranspositionTable():
    def __init__(self) -> None:
        self.zobristTable = self.getZobristTableToJson()
        self.hashTable = self.getHashTableToJson()

    def indexing(self, piece: Piece):
        ''' mapping each piece to a particular number'''
        if piece.type == 'P' and piece.team == True:
            return 0
        if piece.type == 'N' and piece.team == True:
            return 1
        if piece.type == 'B' and piece.team == True:
            return 2
        if piece.type == 'R' and piece.team == True:
            return 3
        if piece.type == 'Q' and piece.team == True:
            return 4
        if piece.type == 'K' and piece.team == True:
            return 5
        if piece.type == 'P' and piece.team == False:
            return 6
        if piece.type == 'N' and piece.team == False:
            return 7
        if piece.type == 'B' and piece.team == False:
            return 8
        if piece.type == 'R' and piece.team == False:
            return 9
        if piece.type == 'Q' and piece.team == False:
            return 10
        if piece.type == 'K' and piece.team == False:
            return 11
        else:
            return -1
    
    def updateHashTable(self, new_hashes: dict):
        connect(db=database_info["db"], host=database_info["host"], port=database_info["port"],
        username=database_info["username"], password=database_info["password"])
        for key in new_hashes:
            try:
                HashTable(
                    hash=key,
                    score=new_hashes[key]["score"],
                    depth=new_hashes[key]["depth"]
                ).save()
            except Exception as e:
                print(e)
        disconnect()
        
    def getHashTableToJson(self):
        zob_dict = {}
        connect(db=database_info["db"], host=database_info["host"], port=database_info["port"],
        username=database_info["username"], password=database_info["password"])
        docs = list(HashTable.objects())
        for obj in docs:
            obj_json = json.loads(obj.to_json())
            zob_dict[obj_json["_id"]] = {
                "score": obj_json["score"],
                "depth": obj_json["depth"]
                }
        disconnect()
        return zob_dict

    def getZobristTableToJson(self):
        connect(db=database_info["db"], host=database_info["host"], port=database_info["port"],
        username=database_info["username"], password=database_info["password"])
        zob_dict = {}
        docs = list(ZobristTable.objects().fields(id=0))
        for obj in docs:
            obj_json = json.loads(obj.to_json())
            zob_dict[obj_json["row"]] = obj_json["cols"]
        disconnect()
        return zob_dict

    def computeHash(self, board):
        h = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    piece = self.indexing(board[i][j])
                    h ^= self.zobristTable[i][j][piece]
        return h

    def generateZobristTable(self):
        connect(db=database_info["db"], host=database_info["host"], port=database_info["port"],
        username=database_info["username"], password=database_info["password"])
        zobTable = [[[random.getrandbits(63) for i in range(12)]for j in range(8)]for k in range(8)]
        for index, row in enumerate(zobTable):
            cols = list()
            for cell in row:
                values = list()
                for value in cell:
                    values.append(value)
                cols.append(values)
            ZobristTable(
                row = index,
                cols = cols
                ).save()
        disconnect()

    

if __name__ == "__main__":
    pass


