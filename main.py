
from pathlib import Path
import shutil

CATEGORIES = {
    "PDFs": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Text_Files": [".txt"],
    "Python_Files": [".py"],
    "Documents": [".doc", ".docx", ".odt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Others": []
}


def get_category(file_path):
    for category, extensions in CATEGORIES.items():
        if file_path.suffix.lower() in extensions:
            return category
    return "Others"


def organize_files(folder):
    folder = Path(folder).expanduser().resolve()

    if not folder.exists() or not folder.is_dir():
        print("Error: Folder does not exist.")
        return

    files = [
        item for item in folder.iterdir()
        if item.is_file()
        and item.name != Path(__file__).name
    ]

    if not files:
        print("No files to organize.")
        return

    print("\nPreview of file organization:")
    for file in files:
        print(f"{file.name} -> {get_category(file)}")

    confirm = input(
        "\nMove these files? Type YES to continue: "
    ).strip()

    if confirm != "YES":
        print("Cancelled. No files were moved.")
        return

    moved = 0

    for file in files:
        category = get_category(file)
        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)

        destination = destination_folder / file.name

        # Avoid overwriting an existing file.
        if destination.exists():
            print(f"Skipped duplicate: {file.name}")
            continue

        try:
            shutil.move(str(file), str(destination))
            moved += 1
            print(f"Moved: {file.name} -> {category}")
        except OSError as error:
            print(f"Could not move {file.name}: {error}")

    print(f"\nFinished! Files moved: {moved}")


def main():
    print("=== SWYNEX File Organizer ===")
    folder = input(
        "Enter the folder path to organize: "
    ).strip().strip('"')

    if not folder:
        print("Please enter a folder path.")
        return

    organize_files(folder)


if __name__ == "__main__":
    main()
