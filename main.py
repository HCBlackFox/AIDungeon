from flask import g
from flask import session
import os
from story.utils import *
import json
from flask import Flask, render_template, request, abort
from story.story_manager import *
import numpy as np
from story.story_manager import *
from generator.gpt2.gpt2_generator import *


"""
generator = GPT2Generator()
    prompt = get_story_start("knight")
    context = get_context("knight")
    story_manager = UnconstrainedStoryManager(generator)
    story_manager.start_new_story(prompt, context=context)

    print("\n")
    print(context)
    print(str(story_manager.story))
    while True:
        action = input("> ")

        if action != "":
            action = action.strip()

            action = action[0].upper() + action[1:]

            action = "\n> " + action + "\n"
            action = remove_profanity(action)
            #action = first_to_second_person(action)
        
        result = story_manager.act(action)
        if player_died(result):
            print(result + "\nGAME OVER")
            break
        else:
            print(result)"""

app = Flask(__name__)
generator = GPT2Generator()
story_manager = UnconstrainedStoryManager(generator)

# Shows about. (Should also link to paper when published)
@app.route('/about.html')
def about():
    return render_template('about.html')

# Bread and butter of app, updates story and returns based on choice
@app.route('/generate', methods=['POST'])
def generate():
    action = request.form["action"]

    # If there is no story in session, make a new one
    if "story" not in session or session["story"] is None:
        print("Starting new story")
        prompt = get_story_start("knight")
        context = get_context("knight")
        story_manager.start_new_story(prompt, context=context)
        response = context + str(story_manager.story)

    # If there is a story in session continue from it.
    else:
        print("Using existing story")
        story = session["story"]
        story_manager.load_story(story, from_json=True)

        if action != "":
            action = action.strip()

            action = action[0].upper() + action[1:]

            action = "\n> " + action + "\n"
            #action = remove_profanity(action)

        response = story_manager.act(action)

    session["story"] = story_manager.json_story()
    print("Returning response")
    return response

# Routes to index
@app.route('/')
def root():
    session["story"] = None
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)