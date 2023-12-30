class Queue:
    __queue = []

    @staticmethod
    def add_player(user_id):
        Queue.__queue.append(user_id)
        if len(Queue.__queue) == 2:
            print(Queue.__queue)
            player_2 = Queue.__queue.pop()
            player_1 = Queue.__queue.pop()
            print(f"Match made: {player_1} - {player_2}")
