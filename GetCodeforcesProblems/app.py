from flask import Flask, render_template, request, send_file
from script import get_unsolved_problems
from helperMethods import *

app = Flask(__name__)


@app.route('/images/<filename>')
def get_image(filename):
    image_path = 'images/' + filename
    return send_file(image_path, mimetype='image/jpeg')


@app.route('/get_problems', methods=['POST'])
def get_problems():
    handles, problem_rate_description, tags_to_include, tags_to_exclude, divs_to_include, problem_index_to_include = (
        extract_request_data(request))

    all_problems = (
        get_unsolved_problems(handles, -1, 9000, 9000, tags_to_include, tags_to_exclude, divs_to_include, problem_index_to_include))

    print('all problems count : ', len(all_problems))
    problems = get_problems_after_filter_rate(problem_rate_description, all_problems)
    tag_list = read_file('tags')

    return render_template('index.html', handles = request.form['handles'], tags_to_include_text = request.form['tags_to_include'], tags_to_exclude_text=request.form['tags_to_exclude'], tagList=tag_list, list=problems)
    

@app.route('/')
def index():
    tagList = read_file('tags')
    return render_template('index.html', tagList = tagList)


@app.template_filter('get_character')
def get_character(character_code):
    return chr(character_code)


if __name__ == '__main__':
    app.run(debug=True)
