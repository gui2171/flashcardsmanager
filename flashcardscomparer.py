import unicodedata
import sys
import os


def normalize_text(text):
    """Normalize text by converting to lowercase and removing diacritics."""
    text = text.lower()
    text = ''.join(
        c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)
    )
    return text.strip()


def read_list_from_file(filename):
    """Reads a list from a file and returns a dictionary mapping the normalized first term to the full line."""
    data_dict = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if ' -- ' in line:
                key, value = line.split(' -- ', 1)
                normalized_key = normalize_text(key.strip())  # Normalize key for better matching
                if normalized_key not in data_dict:
                    data_dict[normalized_key] = line  # Prevent duplicates within the same file
    return data_dict


def write_list_to_file(filename, data_dict):
    """Writes a dictionary's values back to a file."""
    with open(filename, 'w', encoding='utf-8') as file:
        for value in data_dict.values():
            file.write(value + '\n')


def log_to_file(log_message):
    """Logs messages to a log file."""
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message + "\n")
    sys.stdout.write(log_message + "\n")
    sys.stdout.flush()


def save_review_progress(file, last_index):
    """Saves the last reviewed index to history.txt."""
    history = {}
    if os.path.exists("history.txt"):
        with open("history.txt", "r", encoding="utf-8") as history_file:
            for line in history_file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    saved_file, index = parts
                    history[saved_file] = index

    history[file] = str(last_index)

    with open("history.txt", "w", encoding="utf-8") as history_file:
        for saved_file, index in history.items():
            history_file.write(f"{saved_file},{index}\n")


def load_review_progress(file):
    """Loads the last reviewed index from history.txt."""
    if os.path.exists("history.txt"):
        with open("history.txt", "r", encoding="utf-8") as history_file:
            for line in history_file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    saved_file, index = parts
                    if saved_file == file:
                        return int(index)
    return 0


def manual_review(file):
    """Allows the user to manually review and delete entries one by one, resuming from last position."""
    data_dict = read_list_from_file(file)
    keys = list(data_dict.keys())
    updated_dict = data_dict.copy()

    choice = input("Do you want to continue from where you stopped? (y/n): ").strip().lower()
    last_index = load_review_progress(file) if choice == "y" else 0

    log_to_file(f"Starting manual review of {file} from index {last_index}.")

    for i in range(last_index, len(keys)):
        key = keys[i]
        print(f"Reviewing: {data_dict[key]}")
        log_to_file(f"Reviewing: {data_dict[key]}")
        choice = input("Delete this entry? (y/n/stop): ").strip().lower()
        if choice == "y":
            del updated_dict[key]
            log_to_file(f"Deleted: {data_dict[key]}")
        elif choice == "stop":
            save_review_progress(file, i)  # Save exact last position
            log_to_file(f"Manual review of {file} stopped at index {i}.")
            break

    write_list_to_file(file, updated_dict)
    log_to_file(f"Manual review of {file} completed.")


def main():
    file1 = "list1.txt"
    file2 = "list2.txt"

    while True:
        print("\nMenu:")
        print("1. View number of terms in each list")
        print("2. Remove duplicates from List 2 based on List 1")
        print("3. Remove repeated terms from List 1")
        print("4. Remove repeated terms from List 2")
        print("5. Clean both lists and remove all internal duplicates")
        print("6. Manually review and delete entries from a list (resume available)")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            count_entries(file1, file2)
        elif choice == "2":
            remove_duplicates(file1, file2)
        elif choice == "3":
            remove_internal_duplicates(file1)
        elif choice == "4":
            remove_internal_duplicates(file2)
        elif choice == "5":
            remove_internal_duplicates(file1)
            remove_internal_duplicates(file2)
        elif choice == "6":
            list_choice = input("Which list do you want to review? (1 or 2): ").strip()
            if list_choice == "1":
                manual_review(file1)
            elif list_choice == "2":
                manual_review(file2)
            else:
                print("Invalid choice.")
        elif choice == "7":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()





