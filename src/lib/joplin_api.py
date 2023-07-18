import requests

class JoplinAPI:

    def __init__(self, token, api_url = "http://localhost:41184"):
        self.token = token
        self.api_url = api_url

    def request(self, path, parameter = ""):
        response = requests.get(f"{self.api_url}/{path}?token={self.token}{parameter}")
        print(f"{self.api_url}/{path}?token={self.token}{parameter}")
        notes = response.json()

        return notes

    def get_all_notes(self):
        return self.request("notes")
    
    def find_all_topic_notes(self, topic_number):
        notes = []
        page = 1

        while True:
            response = self.request("notes", f"&page={page}")

            matching_notes = [note for note in response["items"] if note["title"].startswith(topic_number)]

            for note in matching_notes:
                notes.append([page, note["id"], note["title"]])

            if not response["has_more"]:
                break

            page += 1

        return notes
    
    def get_note_text(self, id):
        return self.request(f"notes/{id}", "&fields=body")
