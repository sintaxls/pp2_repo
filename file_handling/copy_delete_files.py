# example 1
# with open("file_handling/examplefile.txt", "w") as f:
#   f.write("Woops! I have deleted the content!")

# with open("file_handling/examplefile.txt") as f:
#   print(f.read())


# example 2

# from pathlib import Path
# file_path = Path("file_handling/deleteme.txt")
# if file_path.exists():
#     file_path.unlink()
#     print("Deleted successfully")
# else:
#     print("There is no such file")

# example 3
# from pathlib import Path

# folder_path = Path("file_handling/deleteme")
# if folder_path.is_dir():
#     folder_path.rmdir()
#     print("Directory deleted")
# else:
#     print("Directory not found")

# example 4
# import shutil

# file = "examplefile1.txt"
# destination = f"file_handling/backup_folder/{file}"

# shutil.copy(file, destination)