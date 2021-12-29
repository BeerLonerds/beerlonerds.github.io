import json
import sys

def append_to_json(path, saved_link):
    with open(path, "r+") as f:
        db = json.loads(f.read())
        db.append(saved_link)
        f.seek(0)
        f.write(json.dumps(db, indent=4))

if __name__ == "__main__":
    saved_link = json.loads(sys.argv[1])
    append_to_json("db.json", saved_link)