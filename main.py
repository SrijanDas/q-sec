from flask import Flask, request, jsonify
import requests
import ollama
import re

app = Flask(__name__)





def clean_text(content: str) -> str:
    return content


def get_response_from_ollama(prompt, user_input):
    response = ollama.generate(model="phi3", prompt=f"{prompt}: {user_input}", stream=False)
    return  response.response


def get_tweet_prompt():
    return "Summarize this blog content as a highly engaging Twitter post for maximum reach and virality"


def get_linkedin_prompt():
    return "Summarize this blog content as a highly engaging linkedin post for maximum reach and virality"

@app.route("/")
def hello():
    return "Hello world"

@app.route("/generate-summary", methods=["POST"])
def tweet_generator():
    try:
        category = request.args.get("category")
        data = request.get_json()
        blog_content = data.get("blog_content", "").strip()

        if not blog_content:
            return jsonify({"error": "Blog content is required"}), 400

        prompt = ''
        if category == "tweet":
            prompt = get_tweet_prompt()

        if category == "linkedin":
            prompt = get_linkedin_prompt()

        generated_post = get_response_from_ollama(prompt, blog_content)

        return jsonify({"post": clean_text(generated_post)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
