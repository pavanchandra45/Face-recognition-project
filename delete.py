import pickle
import os
import csv
import shutil

metadata_file = "metadata.pkl"
csv_file = "users.csv"
dataset_path = "C:\\Users\\katep\\OneDrive\\Desktop\\face\\dataset"

# Load metadata
if not os.path.exists(metadata_file):
    print("❌ Metadata file not found!")
else:
    with open(metadata_file, "rb") as f:
        metadata = pickle.load(f)

    print("📋 Current Users:")
    for uid, data in metadata.items():
        print(f"ID: {uid}, Name: {data['Name']}")

    user_id = input("\nEnter the User ID you want to delete: ")

    if user_id in metadata:
        confirm = input(f"Are you sure you want to delete user '{metadata[user_id]['Name']}' (y/n)? ").lower()
        if confirm == 'y':
            # 1. Delete from metadata
            del metadata[user_id]
            with open(metadata_file, "wb") as f:
                pickle.dump(metadata, f)
            print(f"✅ Removed from metadata.pkl")

            # 2. Delete from users.csv
            updated_rows = []
            with open(csv_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] != user_id:
                        updated_rows.append(row)

            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            print(f"✅ Removed from users.csv")

            # 3. Delete user dataset folder
            user_folder = os.path.join(dataset_path, user_id)
            if os.path.exists(user_folder):
                shutil.rmtree(user_folder)
                print(f"✅ Deleted folder: {user_folder}")
            else:
                print("⚠️ No folder found for this user.")

        else:
            print("❌ Deletion cancelled.")
    else:
        print("⚠️ User ID not found in metadata.")
