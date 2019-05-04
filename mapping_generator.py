import csv

DATASET_FILE_NAME = "train_triplets.txt"
USER_TO_SONGS_FILE = "cf_data.csv"
INFO_FILE = "train_triplets_info.txt"
USER_ID_LENGTH = 40
SONG_ID_LENGTH = 18

def createUserSongsMapping(filename):
    '''
    Use the original data given in DATASET_FILE_NAME and write a new file 
    in USER_TO_SONGS_FILE which formats the data in a more efficient way
    to process.
    Also collect information of the dataset and write to INFO_FILE
    '''
    songs, userToListenedSongs = get_users_and_songs(filename)
    write_data_info(songs, userToListenedSongs)
    write_user_songs_map_file(userToListenedSongs)

def write_data_info(songs, userToListenedSongs):
    with open(INFO_FILE, 'w') as outfile:
        outfile.write("Number of users: " + str(len(userToListenedSongs)) + "\n")
        outfile.write("Number of songs: " + str(len(songs)) + "\n")

def write_user_songs_map_file(userToListenedSongs):
    with open(USER_TO_SONGS_FILE, 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')

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

createUserSongsMapping(DATASET_FILE_NAME)