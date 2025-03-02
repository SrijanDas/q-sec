from flask import Flask, request, jsonify
import requests
import ollama
import re

app = Flask(__name__)


def extract_after_think(text):
    match = re.search(r"</think>\s*(.*)", text, re.DOTALL)
    return match.group(1).strip() if match else None


def clean_text(content: str) -> str:
    return content


def get_response_from_ollama(user_input):
    response = ollama.chat(model="deepseek-r1:7b", messages=[{"role": "user", "content": user_input}])

    if 'message' in response:
        return extract_after_think(response['message']['content'])
    else:
        return 'Sorry, something went wrong.'


def get_tweet_prompt(content):
    return f"Rewrite this blog content as a highly engaging Twitter post for maximum reach and virality:\n\n{content}"


def get_linkedin_prompt(content):
    return f"Rewrite this blog content as a highly engaging linkedin post for maximum reach and virality:\n\n{content}"


@app.route("/generate-summary", methods=["POST"])
def tweet_generator():
    try:
        category = request.args.get("category")
        data = request.get_json()
        blog_content = data.get("blog_content", "").strip()
        generated_post = ""

        if not blog_content:
            return jsonify({"error": "Blog content is required"}), 400

        if (category == "tweet"):
            prompt = get_tweet_prompt(blog_content)
            generated_post = get_response_from_ollama(prompt + blog_content)

        if (category == "linkedin"):
            prompt = get_linkedin_prompt(blog_content)
            generated_post = get_response_from_ollama(prompt + blog_content)

        return jsonify({"post": clean_text(generated_post)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
