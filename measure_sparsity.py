import itertools

from recommender import user_to_songs_table

if __name__ == "__main__":
    userToListenedSongs = user_to_songs_table("cf_data.csv")
    all_songs = set(itertools.chain.from_iterable([l for l in userToListenedSongs.values()]))
    num_non_zeroes = sum([len(l) for l in userToListenedSongs.values()])
    print(num_non_zeroes)
    print(len(all_songs) * len(userToListenedSongs))
    print("Sparsity:", num_non_zeroes / (len(all_songs) * len(userToListenedSongs)))
