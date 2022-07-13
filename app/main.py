# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model?
"""

# import basics
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
# import stuff for our models
from aitextgen import aitextgen

# load up a model from memory. Note you may not need all of these options.
#ai = aitextgen(model_folder="model/",
              # tokenizer_file="model/aitextgen.tokenizer.json", to_gpu=False)

ai = aitextgen(model="EleutherAI/gpt-neo-125M", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver
sub_path = ''
def subject_text_generation(subject_type):
    if subject_type == 'Claim':
        file_dest = 'model/claim'
    if subject_type == 'Evidence':
        file_dest = 'model/evidence'
    if subject_type == 'Rebuttal':
        file_dest = 'model/rebuttal'
    if subject_type == 'Conclusion':
        file_dest = 'model/conclusion'
    if subject_type == 'CounterClaim':
        file_dest = 'model/counter'
    return file_dest

@app.route(f'{base_url}')
def home():
    return render_template('index.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))


@app.route(f'{base_url}/results/')
def results():
    if 'data' in session:
        data = session['data']
        print("Data: ",data)
        return render_template('index.html', generated=" ; ".join(i for i in data))
    else:
        return render_template('index.html', generated=None)


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """
    prompt = str(request.form['prompt'])
    subject_type = request.form['subject']
    number = int(request.form['number'])
    sub_path = subject_text_generation(subject_type)
    print("\n\n subject", subject_type, "prompt", prompt, "sub_type", sub_path, "\n\n")
    ai = aitextgen(model_folder = sub_path, to_gpu = False)
    if prompt is not None:
        if subject_type == "Rebuttal":
            generated = ai.generate(
                n=number,
                batch_size=1,
                prompt=prompt,
                max_length=300,
                temperature=0.9,
                return_as_list=True
            )
        elif subject_type == 'Claim':
            generated = ai.generate(
                n=number,
                batch_size=3,
                prompt=prompt,
                max_length=300,
                temperature=0.9,
                return_as_list=True)
        elif subject_type == 'Evidence':
            generated = ai.generate(
                n=number,
                batch_size=3,
                prompt=prompt,
                max_length=300,
                temperature=0.9,
                return_as_list=True)
        elif subject_type == 'CounterClaim':
             generated = ai.generate(
                n=number,
                batch_size=3,
                prompt=prompt,
                max_length=300,
                temperature=0.9,
                return_as_list=True)
        elif subject_type == 'Conclusion':
             generated = ai.generate(
                n=number,
                batch_size=3,
                prompt=prompt,
                max_length=300,
                temperature=0.9,
                return_as_list=True)
    data = {'generated_ls': generated}
    session['data'] = generated[:number + 1]
    # print(*a, sep = "\n")
    return redirect(url_for('results'))

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc20.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
3