from mongoengine import Document, IntField, FloatField, ListField 
from mongoengine import connect, disconnect

from pieces.piece import Piece

class ZobristTable(Document):
    row = IntField(required=True, unique=True)
    cols = ListField(ListField(IntField()))


class HashTable(Document):
    hash = FloatField(required=True, unique=True)
    score = FloatField(required=True)

    
class ZobristClass():
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
    def openConnection(self):
        connect(db="licenta", host="localhost", port=27017, username="AdminMatei", password="pass")
    
    def closeConnection(self):
        disconnect()

    def getAllDocuments(self):
        return list(HashTable.objects().fields(id=0))

    def computeHash(self, board):
        h = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    piece = self.indexing(board[i][j])
                    zobTable = ZobristTable.objects.get(row=i)
                    h ^= int(zobTable.cols[j][piece])
        return h

    def checkHash(self, hash):
        obj = HashTable.objects(hash=hash)
        if len(obj) == 0:
            return False
        return True
    
    def getValueFromHash(self, hash):
        obj = HashTable.objects.get(hash=hash)
        return obj.score
    
    def storeValue(self, hash, score):
        HashTable(
            hash=hash,
            score=score
        ).save()


if __name__ == "__main__":
    import json
    zob = ZobristClass()
    zob.openConnection()
    zob_dict = {}
    docs = zob.getAllDocuments()
    for obj in docs:
        obj_json = json.loads(obj.to_json())
        # print(obj_json["hash"])
        # break
        zob_dict[obj_json["hash"]] = obj_json["score"]

    print(json.dumps(zob_dict, indent=4))


