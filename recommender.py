import math
import csv
import random


def generate_recommendation(active_user, userToListenedSongs, cosine, common_rate, 
                            max_recs, max_sim_user=0, subset_size=1):
    """
    Return a set of recommendations for active_user.
    """
    if max_sim_user == 0:
        max_sim_user = len(userToListenedSongs)
    
    similar_users = []

    # randomly generate a subset instead of using the full dataset
    subset = (userToListenedSongs.keys()
            if subset_size == 1
            else random.sample(userToListenedSongs.keys(), 
                            int(len(userToListenedSongs) * subset_size)))
    
    for user in subset:
        if user != active_user and is_similar(active_user, user, userToListenedSongs, cosine):
            similar_users.append(user)
            if len(similar_users) >= max_sim_user:
                break

    print(len(similar_users), 'similar users')

    recommendations = get_common_songs(similar_users, userToListenedSongs,
                                        common_rate, max_recs)
    return recommendations

def user_to_songs_table(filename):
    """
    Given the dataset specified by the parameter filename, return a mapping
    from a user to all the songs that user listened to in the dataset.
    """
    userToListenedSongs = dict()

    with open(filename, 'r') as data:
        reader = csv.reader(data, delimiter=',')
        for row in reader:
            userToListenedSongs[row[0]] = set(row[1:])

    return userToListenedSongs

def is_similar(user1, user2, userToListenedSongs, cosine):
    """
    Return whether 2 users are similar using the cosine method.
    """
    def dot_product(user1, user2, userToListenedSongs):
        result = 0
        for song in userToListenedSongs[user1]:
            if song in userToListenedSongs[user2]:
                result += 1
        return result

    def magnitude(user, userToListenedSongs):
        return math.sqrt(len(userToListenedSongs[user]))

    result = (dot_product(user1, user2, userToListenedSongs) /
            (magnitude(user1, userToListenedSongs) * magnitude(user2, userToListenedSongs)))

    return result >= cosine

def get_common_songs(similar_users, userToListenedSongs, common_rate, max_recs):
    """
    Return the songs that have been listened to by by more people than the threshold
    common_rate
    First create a songs frequency hash table.
    Then return the ones which appear more than the threshold.
    The max_recs parameter determine the maximum number of songs to return
    """
    common_songs = []

    song_frequency = dict()
    
    for user in similar_users:
        for song in userToListenedSongs[user]:
            if not song in song_frequency:
                song_frequency[song] = 1
            else:
                song_frequency[song] += 1
        
    for song in song_frequency:
        if song_frequency[song] >= common_rate:
            common_songs.append(song)

    if len(common_songs) <= max_recs:
        return common_songs
    common_songs.sort(key=lambda song: song_frequency[song], reverse=True)
    
    return set(common_songs[:max_recs])
    