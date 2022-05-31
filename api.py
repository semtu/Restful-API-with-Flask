import json
from flask import Flask, jsonify, request
import os
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = os.path.join(BASE_DIR, "blogData.json")


def load_json():
    with open(DATA_PATH, "r") as f:
        posts = json.loads(f.read())
    return posts


def number_of_posts():
    # Returns the number of posts or an empty list if there are no post under referenced catergory
    return len(load_json()["posts"])


@app.route("/api/ping", methods=["GET"])
def api_ping():
    posts = load_json()
    if posts:
        return jsonify({"success": True}), 200


@app.route("/api/posts", methods=["GET"])
def api_view_posts():
    tags = request.args.get("tags")
    direction = request.args.get("direction")

    if direction not in ["asc", "dsc", None]:
        return jsonify({"error": "direction parameter is invalid"}), 400

    def process_multiple_tags():
        """This returns a list of all the the posts.
        If two or or more tags are used, the function returns merges the posts for all
        specified tags and removes duplicates."""
        posts = load_json()

        if not tags:
            return posts["posts"]
        else:
            id_list = list()
            total_resp = list()
            for tag in tags.split(","):
                for post_number in range(len(posts["posts"])):
                    if (
                        tag.lower()
                        == posts["posts"][post_number]["tag"].split(" ")[0].lower()
                    ):
                        total_resp.append(posts["posts"][post_number])
            for response in total_resp:
                if response["id"] not in id_list:
                    id_list.append(response["id"])
                else:
                    total_resp.remove(response)
            return total_resp

    def sort_func(direction):
        if direction == "dsc":
            direction = True
        else:
            direction = False

        sorted_list = sorted(
            process_multiple_tags(),
            key=lambda resp_dict: resp_dict["id"],
            reverse=direction,
        )
        return sorted_list

    return jsonify({"posts": sort_func(direction)}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
