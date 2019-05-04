import random
import datetime
import csv
import time

from recommender import generate_recommendation, user_to_songs_table
from hyperparams import subset_sizes, max_sim_users
from test_harness import split_set

def main():
    num_test_users = 25
    num_hidden_vals = 10
    max_recs = 10 * num_hidden_vals
    data_file = "cf_data.csv"
    test_log_file = f"./test_logs_speed/{datetime.datetime.today()}.csv"
    cosine = 0.1
    common_rate = 0.3
    
    userToListenedSongs = user_to_songs_table(data_file)
    results = [[0 for i in range(len(max_sim_users))] for j in range(len(subset_sizes))]
    test_users = random.sample(userToListenedSongs.keys(), num_test_users)

    for i in range(len(subset_sizes)):
        for j in range(len(max_sim_users)):
            print(f"Hyperparameters: max_sim_user = {max_sim_users[j]}, subset_size = {subset_sizes[i]}")
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
                                                        cosine, common_rate, max_recs,
                                                        subset_size=subset_sizes[i],
                                                        max_sim_user=max_sim_users[j])
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

    print("Speed test results:")
    print(results)
    log_results(test_log_file, results, num_test_users, num_hidden_vals)

def log_results(test_log_file, results, num_test_users, num_hidden_vals):
    with open(test_log_file, 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')

        # write header
        writer.writerow([f"Number of users for each test: {num_test_users}"])
        writer.writerow([f"Value of k: {num_hidden_vals}"])
        writer.writerow(['subset_sizes/max_sim_users'] + max_sim_users)

        # write the results
        for i in range(len(results)):
            writer.writerow([subset_sizes[i]] + results[i])

if __name__ == "__main__":
    main()