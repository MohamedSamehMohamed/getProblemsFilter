import requests


def save_all_tags():
    url = f"https://codeforces.com/api/problemset.problems"
    tags = set()
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK":
        for problem in data["result"]["problems"]:
            problem_name = str(problem["contestId"]) + str(problem["index"])
            
            if 'tags' not in problem:
                continue
            problem_tags = problem['tags']
            for tag in problem_tags:
                tags.add(tag)
    write_to_file(tags, 'tags')


def write_to_file(content, file_name):
    file = open(file_name, "w")
    for line in content:
        if line[-1] != '\n':
            line += '\n'
        file.write(line)
    file.close()


def read_file(file_name):
    file = open(file_name, "r")
    # Read the contents of the file
    file_contents = file.readlines()
    # Close the file
    file.close()
    return file_contents


def extract_request_data(request):
    handles_text = request.form['handles']
    handles = handles_text.split(' ')

    problem_rate_description_text = request.form['problem_rate_description']
    if len(problem_rate_description_text) == 0:
        problem_rate_description_text = '1 2000 1'
    problem_rate_description = problem_rate_description_text.split(' ')
    # make sure the problem_rate_description contains a multiple of 3 [minRate maxRate count]
    while len(problem_rate_description) % 3 != 0:
        problem_rate_description.pop()

    tags_to_include = request.form['tags_to_include'].split(',')
    if len(tags_to_include) == 1 and tags_to_include[0] == '':
        tags_to_include.clear()

    tags_to_exclude = request.form['tags_to_exclude'].split(',')
    if len(tags_to_exclude) == 1 and tags_to_exclude[0] == '':
        tags_to_exclude.clear()

    divs_to_include = request.form['divs_to_include'].split(',')

    problem_index_to_include_text = request.form['divs_to_include_Indexes'].split(',')
    problem_index_to_include = ''
    for index in problem_index_to_include_text:
        problem_index_to_include += index

    return (handles, problem_rate_description, tags_to_include, tags_to_exclude, divs_to_include, problem_index_to_include)


def get_problems_after_filter_rate(problem_rate_description, all_problems):
    index = 0
    while index + 3 <= len(problem_rate_description):
        min_rate = int(problem_rate_description[index])
        max_rate = int(problem_rate_description[index + 1])
        count = int(problem_rate_description[index + 2])
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
    return list
