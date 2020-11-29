# Reddit Gender Detector

A Natural Language Processing experiment using reddit as a data source. The aim of this project is to detect the gender and age of a redditor based on their comment or posts.

This has been made for use in other reddit datamining projects, but could be used for more practical applications.

## Data Source

The training set has been collected using the included `download_training.py` script. Currently the following subreddit's have been used as the ground truth source of age and gender:

 - r/r4r (found in `training_data/r4r_12months.csv`)

These subreddits act as the base for the training data set as they contain structured (though potentially untrustworthy) self-identified gender and age.

## License