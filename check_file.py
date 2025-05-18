import os

print("Files in current directory:")
print(os.listdir())

print("\nChecking if airports.dat exists:")
print(os.path.exists("airports.dat"))
