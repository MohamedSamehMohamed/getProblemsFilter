import requests

def get_user_solved_problems(user_handle):
    url = f"https://codeforces.com/api/user.status?handle={user_handle}"
    solvedList = set()
    try:
      response = requests.get(url)
      data = response.json()
      
      if data["status"] == "OK":
          submissions = data["result"]
          for submission in submissions:
              if submission["verdict"] == "OK":
                  problem_name = str(submission["problem"]["contestId"]) + str(submission["problem"]["index"])
                  solvedList.add(problem_name)
      return solvedList
    except:
        return solvedList

def get_users_solved_problems(user_handles):
    problems = set()
    for handle in user_handles:
        solved_problems = get_user_solved_problems(handle)
        for problem in solved_problems:
            problems.add(problem)
    return problems

def has_common_element(list1, list2):
    if len(list1) == 0 or len(list2) == 0:
        return False
    set1 = set(list1)
    set2 = set(list2)
    common_elements = set1.intersection(set2)
    return len(common_elements) > 0

def get_contests_bassed_on_div(divs_list):
    url = f"https://codeforces.com/api/contest.list"
    contest_ids = [] 
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "OK":
            for contest in data["result"]:
                name = contest["name"]
                take = False
                if len(divs_list) == 0:
                    take = True
                for div in divs_list:
                    if div in name:
                        take = True
                        break 
                if take:
                    contest_ids.append(contest["id"])
            return contest_ids
    except:
        return contest_ids


def get_unsolved_problems(user_handles, min_rate, max_rate, count, tags_to_include, tags_to_exclude, divs_list, problem_index_to_include):
    contest_ids_to_include = get_contests_bassed_on_div(divs_list)
    solvedList = get_users_solved_problems(user_handles)
    url = f"https://codeforces.com/api/problemset.problems"
    unsolved_problems = []
    try:
        response = requests.get(url)    
        data = response.json()
        if data["status"] == "OK":
            index = -1
            for problem in data["result"]["problems"]:
                index += 1 
                solved_count = data['result']['problemStatistics'][index]['solvedCount']
                problem_name = str(problem["contestId"]) + str(problem["index"])
                if problem_name in solvedList:
                    continue
                if 'rating' not in problem or 'tags' not in problem:
                    continue
                problem_rate = problem['rating']
                problem_tags = problem['tags']
                contest_id = problem["contestId"]
                problem_index = str(problem["index"])
                if len(problem_index_to_include) > 0 and problem_index not in problem_index_to_include:
                    continue
                if contest_id not in contest_ids_to_include:
                    continue
                if problem_rate < min_rate or problem_rate > max_rate:
                    continue
                if has_common_element(problem_tags, tags_to_exclude):
                    continue
                if len(tags_to_include) > 0 and not has_common_element(problem_tags, tags_to_include):
                    continue
                
                current_problem = {}
                current_problem['rate'] = problem_rate
                current_problem['tags'] = problem_tags
                current_problem['link'] = 'https://codeforces.com/problemset/problem/' + str(problem['contestId']) + '/' + str(problem['index']) 
                current_problem['name'] = str(problem['contestId']) + str(problem['index']) + '  ' + problem['name']
                current_problem['solved_count'] = solved_count
                unsolved_problems.append(current_problem)
                if len(unsolved_problems) == count:
                    break
    except:
        return unsolved_problems
    return unsolved_problems

