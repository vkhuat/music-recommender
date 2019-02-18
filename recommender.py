DATA_FILE = "cf_data.csv"


def generate_recommendation(user_to_recommend, userToListenedSongs):
    similar_users = []
    for user in userToListenedSongs:
        if is_similar(user_to_recommend, user):
            similar_users.append(user)

    recommendations = get_common_songs(similar_users, userToListenedSongs)
    return recommendations

def is_similar(user1, user2):
    return True

def get_common_songs(similar_users, userToListenedSongs):
    '''
    Return the songs that have been listened to by at least 50% of users.
    First create a songs frequency hash table.
    Then return the ones which appear more than the threshold.
    '''
    common_songs = set()
    threshold = len(similar_users // 2)

    song_frequency = dict()
    
    for user in similar_users:
        for song in userToListenedSongs[user]:
            if not song in song_frequency:
                song_frequency[song] = 1
            else:
                song_frequency[song] += 1
        
    for song in song_frequency:
        if song_frequency[song] >= threshold:
            common_songs.add(song)

    return common_songs