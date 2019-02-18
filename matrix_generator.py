import csv

DATASET_FILE_NAME = "train_triplets.txt"
ADJACENCY_LIST_FILE_NAME = "cf_data.csv"
INFO_FILE = "train_triplets_info.txt"
USER_ID_LENGTH = 40
SONG_ID_LENGTH = 18

def createMatrixFromDataFile(filename):
    '''
    create set of songs and dict of user-to-set-of-songs
    go through every entry in the data to fill the above two structures
    Start creating the csv file:
        First row is list of all songs
        Next rows start with song name and for each user in the column,
        search if the the song exist in. If yes 1, if no 0.
    '''
    songs, userToListenedSongs = get_users_and_songs(filename)
    write_data_info(songs, userToListenedSongs)
    write_adjacency_list(userToListenedSongs)

def write_data_info(songs, userToListenedSongs):
    with open(INFO_FILE, 'w') as outfile:
        outfile.write("Number of users: " + str(len(userToListenedSongs)) + "\n")
        outfile.write("Number of songs: " + str(len(songs)) + "\n")

def write_adjacency_list(userToListenedSongs):
    with open(ADJACENCY_LIST_FILE_NAME, 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')

        length = len(userToListenedSongs)
        for user in userToListenedSongs:
            row = [user] + list(userToListenedSongs[user])
            writer.writerow(row)

def get_users_and_songs(filename):
    songs = set()
    userToListenedSongs = dict()

    with open(filename, 'r') as data:
        for entry in data:
            user_id = entry[0:USER_ID_LENGTH]
            song_id = entry[USER_ID_LENGTH + 1:USER_ID_LENGTH + SONG_ID_LENGTH + 1]
            
            songs.add(song_id)
            if not user_id in userToListenedSongs:
                userToListenedSongs[user_id] = set()
            userToListenedSongs[user_id].add(song_id)

    return songs, userToListenedSongs

createMatrixFromDataFile(DATASET_FILE_NAME)