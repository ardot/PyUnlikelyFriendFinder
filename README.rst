===================
Facebook Unlikely Friend Finder
===================

This library finds unlikely friends within a social graph of mutual friends for a calling user. 

The algorithm is as follows:

unlikelyness = (1 + shared_mutual) / (unique_mutual)

Better explanations of this to come.

To Run:
python fullScript.py <ACCESS_TOKEN>

Where <ACCESS_TOKEN> is a facebook access token for the user to be found. 
