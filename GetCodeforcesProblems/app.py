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
    problem_rate_description_text = request.form['problem_rate_description']
    if len(problem_rate_description_text) == 0:
        problem_rate_description_text = '1 2000 1'
    problem_rate_description = problem_rate_description_text.split(' ')
    # make sure the problem_rate_description contains a multiple of 3 [minRate maxRate count]
    while len(problem_rate_description) % 3 != 0:
        problem_rate_description.pop()

    tags_to_include_text = request.form['tags_to_include']
    tags_to_exclude_text = request.form['tags_to_exclude']
    tags_to_include = tags_to_include_text.split(',')
    tags_to_exclude = tags_to_exclude_text.split(',')
    divs_to_include = request.form['divs_to_include'].split(',')
    problem_index_to_include_text = request.form['divs_to_include_Indexes'].split(',')
    problem_index_to_include = ''
    for index in problem_index_to_include_text:
        problem_index_to_include += index
    if len(tags_to_include) == 1 and tags_to_include[0] == '':
        tags_to_include.clear()
    if len(tags_to_exclude) == 1 and tags_to_exclude[0] == '':
        tags_to_exclude.clear()
    list = []
    index = 0
    # get all the problems
    all_problems = get_unsolved_problems(handles, -1, 9000, 9000, tags_to_include, tags_to_exclude, divs_to_include, problem_index_to_include)
    print('all problems count : ', len(all_problems))
    while index + 3 <= len(problem_rate_description):
        min_rate = int(problem_rate_description[index])
        max_rate = int(problem_rate_description[index+1])
        count = int(problem_rate_description[index+2])
        index += 3
        current = []
        for problem in all_problems:
            if min_rate <= problem['rate'] <= max_rate:
                current.append(problem)
                if len(current) == count:
                    break
        print(min_rate, end=' ')
        print(max_rate, end=' ')
        print(count)
        print(len(current))
        list += current
    tagList = read_file('tags')
    return render_template('index.html', handles = handles_text, tags_to_include_text = tags_to_include_text, tags_to_exclude_text=tags_to_exclude_text, tagList=tagList, list=list)
    
@app.route('/')
def index():
    tagList = read_file('tags')
    return render_template('index.html', tagList = tagList)


@app.template_filter('get_character')
def get_character(character_code):
    return chr(character_code)

if __name__ == '__main__':
    app.run(debug=True)
