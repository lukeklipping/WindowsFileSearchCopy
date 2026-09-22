import os
import shutil
import pandas as pd

def rename_files_from_excel(target_dir, excel_path):
  try:
    df = pd.read_excel(excel_path, header=8)
  except Exception as e:
    print(f"Error reading excel file: {e}")
    return

  file_map = {}

  for root, dirs, files in os.walk(target_dir):
    for file in files:
      file_map[file.lower()] = os.path.join(root, file)

  for i, row in df.iterrows():
    original_file = str(row["File Name"]).strip()
    description = str(row("Description")).strip()

    if not original_file:
      continue

    if original_file.lower() in file_map:
      old_path = file_map[original_file.lower()]
      folder_dir = os.path.dirname(old_path)

    _, ext = os.path.splitext(original_file)

    safe_description = (
        description.replace("/", "-")
        .replace("\\", "-")
        .replace(":", "-")
        .strip()
    )

    if not safe_description.lower().endswith(ext.lower()):
      new_filename = f"{safe_description}{ext}"
    else:
      new_filename = safe_description

    new_path = os.path.join(folder_dir, new_filename)

    try:
      os.rename(old_path, new_path)
      print(f"Renamed: '{original_file}' -> '{new_filename}'")
    except Exception as e:
        print(f"Error renaming {original_file}: {e}")
  else:
    print(f"Could not find file: {original_file}")




def search_copy_targeted(source_dir, destination_dir, record_id):
  if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
    print(f"Created destination dir: {destination_dir}")

  if record_id == "0":
    print("Document ID is set to 0 (skipped). No folders will match.")
    return

  target_name = record_id.strip()
  match = False

  print(
      "\nQuick-searching network paths for document ID folder"
      f" '{target_name}'..."
  )

  try:
    # Get the 3 main folders at the root of blserver
    main_folders = [f for f in os.scandir(source_dir) if f.is_dir()]
  except Exception as e:
    print(f"Error reading root directory: {e}")
    return

  for main_folder in main_folders:
    main_path = main_folder.path
    main_name = main_folder.name

    # Root / [Main Folder] / [Document ID]
    direct_path = os.path.join(main_path, target_name)
    if os.path.isdir(direct_path):
      dest_path = os.path.join(destination_dir, target_name)
      try:
        shutil.copytree(direct_path, dest_path, dirs_exist_ok=True)
        print(f"Successfully copied: '{target_name}' from {main_name}")
        match = True
      except Exception as e:
        print(f"Error copying {target_name}: {e}")

    # Root / [Main Folder] / [Attorney Initials Folder] / [Document ID]
    try:
      for sub_item in os.scandir(main_path):
        if sub_item.is_dir():
          attorney_path = sub_item.path
          candidate_path = os.path.join(attorney_path, target_name)

          if os.path.isdir(candidate_path):
            dest_path = os.path.join(destination_dir, target_name)
            try:
              shutil.copytree(candidate_path, dest_path, dirs_exist_ok=True)
              print(
                  f"Successfully copied: '{target_name}' from {main_name} /"
                  f" {sub_item.name}"
              )
              match = True
            except Exception as e:
              print(f"Error copying {target_name}: {e}")
    except Exception:
      # Skip if there is a permission issue 
      continue

  if not match:
    print(f"No folder found matching Document ID: {target_name}")


# --- Inputs ---
print("=== Document ID Folder Search & Copy ===")
print("\nCaution! Confirm PM excel sheet has been printed and saved before running this script.")
directory = input("Enter root directory: ").strip('"')
file_destination = input("Enter destination folder: ").strip('"')
excel_file = input("Enter path to your Excel report (.xlsx): ").strip('"')

record_id = input("PM Record ID (0 to skip): ").strip()

search_copy_targeted(directory, file_destination, record_id)
rename_files_from_excel(file_destination, excel_file)

input("\nDone! Press Enter to exit...")
