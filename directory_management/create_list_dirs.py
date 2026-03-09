# example 1 nested dirs
# from pathlib import Path
# initial_dir = Path("directory_management")

# nested_dir = initial_dir / "dir1" / "dir2" / "dir3"
# nested_dir.mkdir(parents=True, exist_ok=True)


# example 2 list files and folders
# from pathlib import Path
# dir_management = Path("directory_management")

# for i in dir_management.iterdir():
#     if i.is_dir():
#         print(f"DIR {i.name}")
#     else:
#         print(f"FILE {i.name}")


# example 3 find by extension
# from pathlib import Path
# dir_management = Path("directory_management")

# for file_path in dir_management.rglob("*.txt"):
#     print(file_path)

