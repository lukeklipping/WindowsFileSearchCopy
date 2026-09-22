import os
import shutil


def search_copy_targeted(source_dir, destination_dir, document_id):
  if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
    print(f"Created destination dir: {destination_dir}")

  if document_id == "0":
    print("Document ID is set to 0 (skipped). No folders will match.")
    return

  target_name = document_id.strip()
  match = False

  print(
      "\nQuick-searching network paths for document ID folder"
      f" '{target_name}'..."
  )

  try:
    # Get the 3 main folders at the root level
    main_folders = [f for f in os.scandir(source_dir) if f.is_dir()]
  except Exception as e:
    print(f"Error reading root directory: {e}")
    return

  for main_folder in main_folders:
    main_path = main_folder.path
    main_name = main_folder.name

    # Pattern A: Root / [Main Folder] / [Document ID]
    direct_path = os.path.join(main_path, target_name)
    if os.path.isdir(direct_path):
      dest_path = os.path.join(destination_dir, target_name)
      try:
        shutil.copytree(direct_path, dest_path, dirs_exist_ok=True)
        print(f"Successfully copied: '{target_name}' from {main_name}")
        match = True
      except Exception as e:
        print(f"Error copying {target_name}: {e}")

    # Pattern B: Root / [Main Folder] / [Attorney Initials] / [Document ID]
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
      # Skip if there's a permission issue on a subfolder
      continue

  if not match:
    print(f"No folder found matching Document ID: {target_name}")


# --- Inputs ---
directory = input("Enter root directory: ")
file_destination = input("Enter destination folder: ")

document_id = input("PM project ID (0 to skip): ").strip()

search_copy_targeted(directory, file_destination, document_id)