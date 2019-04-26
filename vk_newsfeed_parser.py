import vk
import collections
import time
import datetime
import json


media = [
    {'name': 'lentaru', 'id': -67991642},
    {'name': 'rbc', 'id': -25232578},
    {'name': 'tvrain', 'id': -17568841},
    {'name': 'gazeta', 'id': -20169232},
    {'name': 'znak_com', 'id': -46437317},
    {'name': 'oldlentach', 'id': -29534144},
    {'name': 'novgaz', 'id': -6726778},
    {'name': 'tassagency', 'id': -26284064},
    {'name': 'ria', 'id': -15755094},
    {'name': 'meduzaproject', 'id': -76982440},
    {'name': 'rgru', 'id': -23304496},
    {'name': 'mash', 'id': -112510789},
    {'name': 'vesti', 'id': -24136539},
    {'name': 'true_lentach', 'id': -125004421},
    {'name': 'kpru', 'id': -15722194},
    {'name': 'tj', 'id': -28261334},
]


def auth(app, login, password):
    session = vk.AuthSession(app_id=app, user_login=login, user_password=password) 
    return vk.API(session) 
  

def get_newsfeed(api, query, data):
    for i in range(0, 1000, 200):
        row = api.newsfeed.search(q=query, count=200, offset=i, v='3.0')
        for item in row[1:]:
            data.append(item)
    return data


def get_wall(api, owner_id, data):
    i = 0
    ts = 1542240000
    curr_date = 1556323200
    while (curr_date > ts):
        row = api.wall.get(owner_id=owner_id, count=1000, offset=i, v='3.0')
        for item in row[1:]:
            data.append(item)
            curr_date = item['date']
        i += 1000
        time.sleep(1)
    return data


def search_wall(api, owner_id, q, data):
    i = 0
    ts = 1542240000
    curr_date = 1556323200
    while (curr_date > ts):
        row = api.wall.search(owner_id=owner_id, query=q, count=100, offset=i, v='3.0')
        for item in row[1:]:
            data.append(item)
            curr_date = item['date']
        i += 100
        time.sleep(1)
    return data
    
    
def get_user(api, user_id):
    return api.users.get(user_ids=user_id, fields=['sex', 'bdate', 'city', 'country', 'home_town'], v='3.0')

    
def get_comments(api, post_id, owner_id):
    return api.wall.getComments(post_id=post_id, owner_id=owner_id, v='3.0')


def modify_date(timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    return value.strftime('%Y-%m-%d %H:%M:%S')


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
        
        
def parse_posts_with_keywords(api, filename):
    keywords = ['автономный рунет']
    data = []
    for word in keywords:
        data = get_newsfeed(api, word, data)
    write_json(data, filename)
    return data


def parse_posts_from_wall(api, owner_id, filename):
    posts = []
    posts = get_wall(api, owner_id, posts)
    write_json(posts, filename)
    return posts


def parse_comments(api, data, filename):
    comments = []
    for i in range(1, len(data)):
        try:
            row = get_comments(api, data[i]['id'], data[i]['owner_id'])
        except:
            row = [0]
        if len(row) > 1:
            for item in row[1:]:
                comments.append(item)
    write_json(comments, filename)
    return comments


def parse_users(api, data, field, users, filename):
    if len(data) > 0:
        users_ids = list(set([item[field] for item in data]))
        users = users + get_user(api, users_ids[:1000])
        if len(users_ids) > 1000:
            users = users + get_user(api, users_ids[1001:])
        write_json(users, filename)
    return users
