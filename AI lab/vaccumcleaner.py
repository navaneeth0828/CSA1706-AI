rooms = ['Dirty', 'Dirty']

location = 0

while location < len(rooms):

    if rooms[location] == 'Dirty':
        print("Cleaning Room", location+1)
        rooms[location] = 'Clean'
    else:
        print("Room", location+1, "Already Clean")

    location += 1

print("Final State:", rooms)
