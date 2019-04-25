import vk
import collections
import time
import datetime
import json


def auth(app, login, password):
    session = vk.AuthSession(app_id=app, user_login=login, user_password=password)
    return vk.API(session)


def get_newsfeed(api, query, data):
    for i in range(0, 1000, 200):
        row = api.newsfeed.search(q=query, count=200, offset=i, v='3.0')
        for item in row[1:]:
            data.append(item)
        time.sleep(1)
    return data


def get_wall(api, owner_id, data):
    for i in range(0, 10000, 1000):
        row = api.wall.get(owner_id=owner_id, offset=i, v='3.0')
        for item in row[1:]:
            data.append(item)
        time.sleep(1)
    return data


def get_user(api, user_id):
    return api.users.get(user_ids=[user_id], fields=['sex', 'bdate', 'city', 'country', 'home_town'], v='3.0')


def get_comments(api, post_id, owner_id):
    return api.wall.getComments(post_id=post_id, owner_id=owner_id, v='3.0')


def modify_date(timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    return value.strftime('%Y-%m-%d %H:%M:%S')


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


api = auth(auth_data['app_id'], auth_data['login'], auth_data['password'])


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
    users_ids = [item[field] for item in data]
    users = users + get_user(api, users_ids[:1000])
    if len(users_ids > 1000):
        users = users + get_user(api, users_ids[1001:])
    write_json(users, filename)
    return users
