# Music Recommendation Using Collaborative Filtering

This project is an implementation of the collaborative filtering algorithm for recommender systems, with optimization methods to improve the runtime. The dataset used for the project is the Echo Nest Taste Profile Subset, which can be found [here](https://labrosa.ee.columbia.edu/millionsong/tasteprofile).

## Code Description
The file `recommender.py` contains implementation of the collaborative filtering algorithm with methods to improve the runtime.

The file `test_harness.py` tests for the accuracy of the algorithm with different hyperparameters measured by the precision and recall rates; while `speed_log.py` records the runtime of the algorithm.

The code in `mapping_generator.py` is used to convert the original data to a format that is faster for the program to convert to a user-to-listened-songs mapping and therefore reduce the runtime.

## How to Run the Code
To run the code, you will first need to download the Echo Nest Taste Profile Subset by going to [this link](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/challenge/train_triplets.txt.zip) and put it in the same folder as the project. Then, run `mapping_generator.py` to convert the data to a different format, which will be stored as `cf_data.csv`. The test logs for this file are generated in the `test_logs` folder.

To run the test using the full dataset with no limits on the number of similar users, run `test_harness.py`. To test the methods used to improve runtime with different parameters, run the file `speed_log.py`. The test logs for this file are generated in the `test_logs_speed` folder.