from models import *

if __name__ == '__main__':
    pass

rover = RoverModel(1, 2, 3)

hiddenPropertiesAlias1 = rover.hiddenProperties
hiddenPropertiesAlias2 = rover.hiddenProperties
print(rover.hiddenProperties)

hiddenPropertiesAlias1.position = 2
print(rover.hiddenProperties)

hiddenPropertiesAlias1.position = 3
print(rover.hiddenProperties)

hiddenPropertiesAlias1.position = 4
hiddenPropertiesAlias2.position = 3
print(rover.hiddenProperties)

