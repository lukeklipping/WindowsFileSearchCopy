import os
import shutil


def search_copy(source_dir, destination_dir, document_id):

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Created desinationd dir: {destination_dir}")

    if document_id == 0:
        print("Document ID is set to 0 (skipped). No folders will match.")
        return

  # Format document ID to string (e.g., 12345.0 -> "12345")
    doc_str = (
        str(int(document_id)) if document_id.is_integer() else str(document_id)
    )
    match = False
    print(f"\nScanning '{source_dir}' for folder name: '{doc_str}'...")

    for root, dirs, files in os.walk(source_dir):
        for dir_name in dirs:
            if dir_name.strip() == doc_str:
                folder_path = os.path.join(root, dir_name)
                dest_path = os.path.join(destination_dir, dir_name)

                try:
                    shutil.copytree(folder_path, dest_path, dirs_exist_ok=True)
                    print(f"Found path and copied to {dir_name}")
                    match = True
                except Exception as e:
                    print(f"Error copying {dir_name}: {e}")

    if not match:
        print(f"No folder found matching Document ID: {doc_str}")





directory = input("Enter root directory: ")
file_destination = input("Enter destination folder: ")

document_id = float(input("PM project ID (0 to skip): "))

search_copy(directory, file_destination, document_id)

