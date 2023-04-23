import tornado.web
import tornado.websocket
import tornado.ioloop
import queue

START = 110
WINNER = 104
LOSER = 104
WAIT = bytes([0, 0, 0])
BIN_MESSAGES = [0, 0, 0]
TEAM1WIN = 105
TEAM2WIN = 106

b1=''
b2=''
b3=''
b4=''
b5=''
b6=''
team1_points=0
team2_points=0

b1_t1 = 3
b1_t2 = 3
b2_t1 = 3
b2_t2 = 3
b3_t1 = 3
b3_t2 = 3

class Room:
    counter = 0
    container = {}

    def __init__(self, handler):
        Room.counter += 1
        self.id = Room.counter
        Room.container[self.id] = handler

    @staticmethod
    def get_the_player(id_of_player):
        return Room.container[id_of_player]

class Game:
    waiting_room = queue.Queue()

    @staticmethod
    def start(game_id):
        if Game.waiting_room.empty():
            Game.waiting_room.put(game_id)
            return None, None
        else:
            player2_id = Game.waiting_room.get()
            game_ids = [game_id, player2_id]
            game_ids_to_bytes = bytes(game_ids)
            player1_id = Game(game_ids_to_bytes)
            return player1_id, player2_id

    def __init__(self, ids: bytes):
        self.id = ids


class MainHandler(tornado.websocket.WebSocketHandler):
    game_id = -1

    def open(self):
        s = Room(handler=self)
        self.game_id = s.id
        print("open")

    def on_close(self):
        print("close")

    def on_message(self, message):
        global team1_points
        global team2_points
        global b1_t1
        global b1_t2
        global b2_t1
        global b2_t2
        global b3_t1
        global b3_t2
        global b1
        global b2
        global b3
        global b4
        global b5
        global b6
        binary_message = list(bytes(message, 'utf-8'))
        print(str(binary_message[0]), str(binary_message[1]), str(binary_message[2]))
        game_list = [binary_message[0], binary_message[1]]
        game_list.sort()
        game_id = bytes(game_list)
        if binary_message == BIN_MESSAGES:
            player1_id, player2 = Game.start(self.game_id)
            if player1_id:
                to_send = [self.game_id, player2, START]
                to_send_player2 = [player2, self.game_id, START]
                self.write_message(bytes(to_send))
                Room.get_the_player(player2).write_message(bytes(to_send_player2))
            else:
                self.write_message(WAIT)

        if binary_message[0] == 1:
            print("ruch twoj")
            if binary_message[2]==1:
                b1 = 'PAPIER'
            if binary_message[2]==2:
                b1 = 'KAMIEN'      
            if binary_message[2]==3:
                b1 = 'NOZYCE'      
        if binary_message[0] == 2:
            print("ruch przeciwnika")
            if binary_message[2]==1:
                b2 = 'PAPIER'
            if binary_message[2]==2:
                b2 = 'KAMIEN'   
            if binary_message[2]==3:
                b2 = 'NOZYCE'    
        if binary_message[0] == 3:
            print("ruch twoj")
            if binary_message[2]==1:
                b3 = 'PAPIER'
            if binary_message[2]==2:
                b3 = 'KAMIEN'      
            if binary_message[2]==3:
                b3 = 'NOZYCE'      
        if binary_message[0] == 4:
            print("ruch przeciwnika")
            if binary_message[2]==1:
                b4 = 'PAPIER'
            if binary_message[2]==2:
                b4 = 'KAMIEN'   
            if binary_message[2]==3:
                b4 = 'NOZYCE'          
        if binary_message[0] == 5:
            print("ruch twoj")
            if binary_message[2]==1:
                b5 = 'PAPIER'
            if binary_message[2]==2:
                b5 = 'KAMIEN'      
            if binary_message[2]==3:
                b5 = 'NOZYCE'      
        if binary_message[0] == 6:
            print("ruch przeciwnika")
            if binary_message[2]==1:
                b6 = 'PAPIER'
            if binary_message[2]==2:
                b6 = 'KAMIEN'   
            if binary_message[2]==3:
                b6 = 'NOZYCE'   

        if(b1 and b2)!='':
             if (b1=="PAPIER" and b2=="KAMIEN") or (b1=="KAMIEN" and b2=="NOZYCE") or (b1=="NOZYCE" and b2=="PAPIER"):

                Room.get_the_player(1).write_message(bytes([1, 0, WINNER]))
                b1=''
                b1=''
                b1_t1=1
                b2_t1=0
             if (b2=="PAPIER" and b1=="KAMIEN") or (b2=="KAMIEN" and b1=="NOZYCE") or (b2=="NOZYCE" and b1=="PAPIER"):
                Room.get_the_player(2).write_message(bytes([2, 0, WINNER]))   
                b2_t1=1
                b1_t1=0

        if(b3 and b4)!='':
             if (b3=="PAPIER" and b4=="KAMIEN") or (b3=="KAMIEN" and b4=="NOZYCE") or (b3=="NOZYCE" and b4=="PAPIER"):
                Room.get_the_player(3).write_message(bytes([3, 0, WINNER]))
                b1_t2=1
                b2_t2=0

             if (b4=="PAPIER" and b3=="KAMIEN") or (b4=="KAMIEN" and b3=="NOZYCE") or (b4=="NOZYCE" and b3=="PAPIER"):  
                Room.get_the_player(4).write_message(bytes([4, 0, WINNER]))   
                b2_t2=1
                b1_t2=0

        if(b5 and b6)!='':
             if (b5=="PAPIER" and b6=="KAMIEN") or (b5=="KAMIEN" and b6=="NOZYCE") or (b5=="NOZYCE" and b6=="PAPIER"):
                Room.get_the_player(5).write_message(bytes([5, 0, WINNER]))
                b3_t1=1
                b3_t2=0
             if (b6=="PAPIER" and b5=="KAMIEN") or (b6=="KAMIEN" and b5=="NOZYCE") or (b6=="NOZYCE" and b5=="PAPIER"):
                Room.get_the_player(6).write_message(bytes([6, 0, WINNER]))   
                b3_t2=1
                b3_t1=0


        if(b1_t1 ==1 and b1_t2 ==1 and b3_t1 == 1 and b2_t1 ==0 and b2_t2 ==0 and b3_t2 ==0) or (b1_t1 ==1 and b1_t2 ==0 and b3_t1 == 1 and b2_t1 ==0 and b2_t2 == 1 and b3_t2 ==0) or (b1_t1 ==0 and b1_t2 ==1 and b3_t1 == 1 and b2_t1 ==1 and b2_t2 ==0 and b3_t2 ==0) or (b1_t1 ==1 and b1_t2 ==1 and b3_t1 == 1 and b2_t1 ==0 and b2_t2 ==0 and b3_t2 ==1):
            print("Team nr 1 wygrywa!")   
            for i in range(1,7):
                Room.get_the_player(i).write_message(bytes([i, 0, TEAM1WIN]))
        if(b1_t1 ==0 and b1_t2 ==0 and b3_t1 == 0 and b2_t1 ==1 and b2_t2 ==1 and b3_t2 ==1) or (b1_t1 ==0 and b1_t2 ==1 and b3_t1 == 0 and b2_t1 ==1 and b2_t2 ==0 and b3_t2 ==1) or (b1_t1 ==1 and b1_t2 ==0 and b3_t1 == 0 and b2_t1 ==0 and b2_t2 ==1 and b3_t2 ==1) or (b1_t1 ==0 and b1_t2 ==0 and b3_t1 == 1 and b2_t1 ==1 and b2_t2 ==1 and b3_t2 ==0):
            print("Team nr 1 wygrywa!") 
            for i in range(1,7):
                Room.get_the_player(i).write_message(bytes([i, 0, TEAM2WIN]))

    def check_origin(self, origin):
        print("ORIGIN: ", origin)
        return True

def main():
    app = tornado.web.Application([
        ("/ws", MainHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
