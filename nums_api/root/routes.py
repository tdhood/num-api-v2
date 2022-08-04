from flask import Blueprint, render_template
import markdown

root = Blueprint("root", __name__)

@root.get('/')
def home_page():
    """Homepage: renders the landing page for Numbers Api"""

    # Reads in the api_docs.md file and converts it to a string of html.
    with open("nums_api/api_docs.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text, output_format='xhtml')

    return render_template('index.html', docs=html)
