import os
import sys
import re
import csv

from process_line import process_line

GAME_PATH = 'games.csv'
HANDS_PATH = 'hands.csv'

def normalize_path(path):
    if not os.path.isabs(path):
        return os.path.abspath(path)
    else:
        return path
    
def process_game_details(filename):
    pattern = r'HH(?P<start_date>\d{8}-\d{6})\s-\s(?P<id>\d+)\s-\s(?P<type>.*)\s-\s(?P<stakes>.*)\s-\s.*'
    result = re.search(pattern, filename)
    return result.groupdict()

if __name__ == "__main__":
    target_path = normalize_path(sys.argv[1])
    games = []
    dumbo_flag = True
    for filename in sorted(os.listdir(target_path)):
        if filename.startswith('HH'):
            file_path = os.path.join(target_path, filename)
            game_details = process_game_details(filename)
            hands = []

            with open(file_path, 'r') as f:

                curr_hand = None
                for line in f:
                    new_hand = process_line(line, curr_hand)
                    if new_hand is not None:
                        if curr_hand is not None:
                            curr_hand["game_id"] = game_details["id"]
                            hands.append(curr_hand)
                        curr_hand = new_hand
                hands.append(curr_hand)
            with open(HANDS_PATH, 'a+') as hands_file:
                writer = csv.DictWriter(hands_file, fieldnames=hands[0].keys())
                if dumbo_flag:
                    writer.writeheader()
                    dumbo_flag = False
                writer.writerows(hands)

            game_details["win/loss"] = sum([h["net"] for h in hands])
            games.append(game_details)
    with open(GAME_PATH, 'w+') as games_file:
        writer = csv.DictWriter(games_file, fieldnames=games[0].keys())
        writer.writeheader()
        writer.writerows(games)

                    
                    

                


