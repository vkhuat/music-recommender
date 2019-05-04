import random
import datetime
import csv
import time

from recommender import generate_recommendation, user_to_songs_table
from hyperparams import cosines, common_rates

def main():

    """
    Test design:
    - Select the values from the hyperparameter space.
    - Select a set of users to test (more users take more time)
    - Pick a user.
    - Hide 10 songs from the list of songs they listened to.
    - Generate recommendations for them.
    - Calculate precision/recall rates
    - Record that.
    """
    num_test_users = 25
    num_hidden_vals = 10
    max_recs = 10 * num_hidden_vals
    data_file = "cf_data.csv"
    test_log_file = f"./test_logs/{datetime.datetime.today()}.csv"
    
    userToListenedSongs = user_to_songs_table(data_file)
    results = [[0 for i in range(len(cosines))] for j in range(len(common_rates))]
    test_users = random.sample(userToListenedSongs.keys(), num_test_users)

    for i in range(len(common_rates)):
        for j in range(len(cosines)):
            print(f"Hyperparameters: cosine = {cosines[j]}, common_rate = {common_rates[i]}")
            total_recs = 0      # number of recommendations generated.
            num_recalled = 0    # number of items successfully recalled.
            num_hidden = 0      # total number of values hidden.
            avg_time = 0

            for user in test_users:
                all_items = userToListenedSongs[user]
                hidden_items, remaining_items = split_set(all_items, num_hidden_vals)
                
                userToListenedSongs[user] = remaining_items

                start = time.time()
                recommendations = generate_recommendation(user, userToListenedSongs,
                                                        cosines[j], common_rates[i], max_recs)
                end = time.time()

                
                # Count how many items successfully recalled for this user and add to the
                # total number of values recalled.
                num_recalled += len({item for item in hidden_items if item in recommendations})
                total_recs += len(recommendations)
                num_hidden += len(hidden_items)
                exec_time = end - start
                avg_time += exec_time

                # change the data back
                userToListenedSongs[user] = all_items

            precision = 0 if total_recs == 0 else num_recalled / total_recs     # set precision to 0 if the algorithm produces 0 recommendations in total.
            recall = num_recalled / num_hidden
            avg_time /= num_test_users
            results[i][j] = f"{precision} / {recall} / {avg_time}"
    
    print("Test harness results:")
    print(results)
    log_results(test_log_file, results, num_test_users, num_hidden_vals)

def log_results(test_log_file, results, num_test_users, num_hidden_vals):
    with open(test_log_file, 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')

        # write header
        writer.writerow([f"Number of users for each test: {num_test_users}"])
        writer.writerow([f"Value of k: {num_hidden_vals}"])
        writer.writerow(['common_rate/cosine'] + cosines)

        # write the results
        for i in range(len(results)):
            writer.writerow([common_rates[i]] + results[i])

def split_set(s, num_hidden_values):
    if len(s) <= num_hidden_values:
        return (set(), s)

    hidden_items = set(random.sample(s, num_hidden_values))
    remaining_items = {item for item in s if item not in hidden_items}

    return (hidden_items, remaining_items)

if __name__ == "__main__":
    main()