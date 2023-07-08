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