import json
import sys

def load_saved_link(event_path):
    with open(event_path) as f:
        webhook_payload = json.load(event_path)
        return webhook_payload["inputs"]["link"]

def append_to_json(path, saved_link):
    with open(path, "r+") as f:
        db = json.loads(f.read())
        db.append(saved_link)
        f.seek(0)
        f.write(json.dumps(db, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    gh_event_path = sys.argv[1]
    saved_link = load_saved_link(gh_event_path)
    append_to_json("data/db.json", saved_link)
