import os

class ObsidianAPI:

    def __init__(self):
        self.note_path = ""

    def findNote(self, path, name):
        for root, dirs, files in os.walk(path):
            if name in files:
                note_path = os.path.join(root, name)
                return note_path
        return None

    def find_all_topic_notes(self, note_path, topic):
        matching_files = []

        for dirpath, _, filenames in os.walk(note_path):
            for filename in filenames:
                if filename.endswith(".md"):
                    full_filepath = os.path.join(dirpath, filename)
                    try:
                        with open(full_filepath, 'r', encoding='utf-8') as file:
                            content = file.read()
                            if topic in content:
                                matching_files.append(full_filepath)
                    except Exception as e:
                        print(f"Error reading {full_filepath}: {e}")

        return matching_files
    
    def get_note_text(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()