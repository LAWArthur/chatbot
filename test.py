from wxpy import *
from os import *

#initialize the robot
bot = Bot(cache_path=True)
 
# get all the friends
myFriends = bot.friends()
print(type(myFriends))

sex_dict = {'male':0,'female':0}
for friend in myFriends:
    if friend.sex == 1:
        sex_dict['male'] +=1
    elif friend.sex ==2:
        sex_dict['female'] +=1
print(sex_dict)