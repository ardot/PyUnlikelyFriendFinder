#!/usr/bin python

import facebook
import constants
import bitarray
import csv
import sys
import os.path
import ast
import heapq
import math

# Holds the indeces of each FB friend
indeces = {}
# Remembers which mutual friendships have already been checked
checked = {}
# Stores who is friends with who else!
mutual_friendships = {}
# Stores bitarrays with that same data
mutual_friendships_bit = {}
# Stores the list of friends, ordered by friend id
raw_friends = []
# Number of mutual friends for any given friend
num_mutual = {}
# Heap the track the most unexpected friends
heap = []

# graph = facebook.GraphAPI(constants.oauth)
# profile = graph.get_object("me")
# friends = graph.get_connections("me", "friends")
# raw_friends = friends['data']


# Prevent the program from downloading the mutual friendlist repeated, as this
# takes forever
if (len(sys.argv) > 1 and sys.argv[1] == "rescrape") or not os.path.isfile("mutual_friendships.csv") or not os.path.isfile("indeces.csv"):
  graph = facebook.GraphAPI(constants.oauth)
  profile = graph.get_object("me")
  friends = graph.get_connections("me", "friends")
  raw_friends = friends['data']


 # init the data structures
  counter = 0
  for friend in raw_friends:
    friend_id = friend['id']
    indeces[friend_id] = counter
    counter = counter + 1

  length = len(raw_friends)

  counter = 0
  for friend in raw_friends:
    # Init a bit array to store mutual friendships
    friend_id = friend['id']
    friend_adjacencies = bitarray.bitarray(length)
    # Get mutual friends
    mutual = graph.get_connections(friend_id, "mutualfriends")
    raw_mutual = mutual['data']
    raw_mutual_list = []
    for mutual_friend in raw_mutual:
      mutual_friend_id = mutual_friend['id']
      raw_mutual_list.append(mutual_friend_id)
      index = indeces[mutual_friend_id]
      friend_adjacencies[index] = 1
    mutual_friendships[friend_id] = raw_mutual_list
    mutual_friendships_bit[friend_id] = friend_adjacencies
    print "Done one!" + str(counter)
    counter = counter + 1

  print str(mutual_friendships_bit)

  w = csv.writer(open("mutual_friendships.csv", "w"))
  for key, val in mutual_friendships.items():
      w.writerow([key, val])
  w = csv.writer(open("mutual_friendships_bit.csv", "w"))
  for key, val in mutual_friendships_bit.items():
      w.writerow([key, val])
  w = csv.writer(open("indeces.csv", "w"))
  for key, val in indeces.items():
    w.writerow([key,val])

# When the data has already been scraped
else:
  for key, val in csv.reader(open("mutual_friendships.csv")):
    mutual_friendships[key] = ast.literal_eval(val)
  for key, val in csv.reader(open("mutual_friendships_bit.csv")):
    mutual_friendships_bit[key] = eval('bitarray.' + val)
  for key, val in csv.reader(open("indeces.csv")):
    indeces[key] = ast.literal_eval(val)
  with open('raw_friends.csv') as f:
    raw_friends = f.read().splitlines()


for friend in raw_friends:
  friend_data = ast.literal_eval(friend)
  friend_id = friend_data['id']
  friend_bits = mutual_friendships_bit[friend_id]
  # Count the number of mutual friends the current friend has
  if friend_id not in num_mutual:
    num_mutual[friend_id] = friend_bits.count()

  for mutual_friend in mutual_friendships[friend_id]:
    if (mutual_friend, friend_id) not in checked:
      # And 'em
      friend_bits = mutual_friendships_bit[friend_id]
      mutual_bits = mutual_friendships_bit[mutual_friend]
      and_bits = friend_bits & mutual_bits
      # Count shared friends an no of mutual friends
      counter = 0
      # If mutual bits have not already been counted
      if mutual_friend not in num_mutual:
        num_mutual[mutual_friend] = mutual_bits.count()
      # Count the number of shared mutual friends
      and_bit_count = and_bits.count()
      # Calculate the metric:


      # metric = float(and_bit_count) / (num_mutual[friend_id] + num_mutual[mutual_friend])

      # metric = float((num_mutual[friend_id] - and_bit_count) + (num_mutual[mutual_friend] - and_bit_count))
      # metric = metric / float((num_mutual[friend_id] + num_mutual[mutual_friend]))
      # metric = 1 / float(metric)

      # metric = float(num_mutual[friend_id]) / num_mutual[mutual_friend]
      # metric = max(metric, (1/metric))

      # metric = float(and_bit_count)

      # metric = float(and_bit_count) / num_mutual[friend_id] + float(and_bit_count) / num_mutual[mutual_friend]
      heapq.heappush(heap, (metric, (friend_id, mutual_friend)))
      checked[(friend_id, mutual_friend)] = 1

id_to_name = {}
for friend in raw_friends:
  friend_data = ast.literal_eval(friend)
  id_to_name[friend_data['id']] = friend_data['name']

for i in range(1,30):
  (c, (f1,f2)) =  heapq.heappop(heap)
  coefficient = float(c)
  friend_one = id_to_name[f1]
  friend_two = id_to_name[f2]
  print friend_one + " and " + friend_two + " with coefficient " + str(coefficient)

#  print friend_data['id']
# mutual_with_imran= graph.get_connections("100004234592345", "mutualfriends")['data']
#print mutual_with_imran
