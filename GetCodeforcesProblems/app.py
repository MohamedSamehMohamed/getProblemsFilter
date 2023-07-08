from flask import Flask, render_template, request, send_file
from script import get_unsolved_problems
from helperMethods import *

app = Flask(__name__)

@app.route('/images/<filename>')
def get_image(filename):
    image_path = 'images/' + filename  # Replace with the actual path
    return send_file(image_path, mimetype='image/jpeg')

@app.route('/get_problems', methods=['POST'])
def get_problems():
    handles_text = request.form['handles']
    handles = handles_text.split(' ')
    min_rate = int(request.form['min_rate'])
    max_rate = int(request.form['max_rate'])
    page = int(request.form['page'])
    tags_to_include_text = request.form['tags_to_include']
    tags_to_exclude_text = request.form['tags_to_exclude']
    tags_to_include = tags_to_include_text.split(',')
    tags_to_exclude = tags_to_exclude_text.split(',')
    if len(tags_to_include) == 1 and tags_to_include[0] == '':
        tags_to_include.clear()
    if len(tags_to_exclude) == 1 and tags_to_exclude[0] == '':
        tags_to_exclude.clear()
        
    list = get_unsolved_problems(handles, min_rate, max_rate, tags_to_include, tags_to_exclude)
    tagList = read_file('tags')
    return render_template('index.html', handles = handles_text, min_rate = min_rate, max_rate = max_rate, tags_to_include_text = tags_to_include_text, tags_to_exclude_text = tags_to_exclude_text, tagList = tagList, list = list)
    
@app.route('/')
def index():
    tagList = read_file('tags')
    return render_template('index.html', tagList = tagList)

if __name__ == '__main__':
    app.run(debug=True)
