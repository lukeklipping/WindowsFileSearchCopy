import os
import shutil


def search_copy(source_dir, destination_dir, document_id):

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Created desinationd dir: {destination_dir}")

    if document_id == "0":
        print("Document ID is set to 0 (skipped). No folders will match.")
        return

    match = False
    target_name = document_id.strip()

    for root, dirs, files in os.walk(source_dir):
        if target_name in dirs:
            folder_path = os.path.join(root, target_name)
            dest_path = os.path.join(destination_dir, target_name)

            try:
                shutil.copytree(folder_path, dest_path, dirs_exist_ok=True)
                print(f"Successfully copied: '{target_name}' from {root}")                
                match = True
            except Exception as e:
                print(f"Error copying {target_name}: {e}")

    if not match:
        print(f"No folder found matching Document ID: {document_id}")





directory = input("Enter root directory: ")
file_destination = input("Enter destination folder: ")

document_id = input("PM project ID (0 to skip): ").strip()

search_copy(directory, file_destination, document_id)

