#!/usr/bin/env python
from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
import json

app = Flask(__name__)
api = Api(app)

users=[{'first_name':'farid','last_name':'','user_id':'fsaad','groups':[]}]
fields=['first_name','last_name','user_id','groups']
groups=['admins','dev','ops']

def add_user(record):
    global users
    users.append(record)
    return record

def get_user(user_id):
    for user in users:
        if (user.has_key('user_id') and user['user_id']==user_id):
            return user
    return None

def delete_user(user_id):
    for user in users:
        if (user.has_key('user_id') and user['user_id']==user_id):
            users.remove(user)
            return True

def update_user(user_id):
    for user in users:
        if (user.has_key('user_id') and user['user_id']==user_id):
            users.remove(user)

## TODO:
## Return member list of group when exists.
def get_group(group):
    if group in groups:
        return True
    else:
        return None
        
def add_group(group):
    groups.append(group)
    return group

def delete_group(group_id):
    remove_group_from_users(group_id)
    groups.remove(group_id)
    return True

def valid_record(record):
    for field in fields: 
        if record[field] is None:
            return None
    return True

def add_group_to_members(group, members):
    for user in users:
        if user['user_id'] in members and group not in user['groups']:
            user['groups'].append(group)
    return True

def remove_group_from_users(group_id):
    for user in users:
        if group_id in user['groups']:
            user['groups'].remove(group_id)
    return True

def get_users_in_group(group_id):
    users_in_group=list()
    for user in users:
        if group_id in user['groups']:
            users_in_group.append(user['user_id'])
    return users_in_group

class UserList(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('user_id')
        # https://github.com/flask-restful/flask-restful/issues/380
        parser.add_argument('groups', type=list, location=['json'],default=[])
        args = parser.parse_args()
        if valid_record(args) == None:
            return abort(409, message="Fields missing")
        elif get_user(args['user_id']) is not None:
            return abort(409, message="User already exists")
        else:
            return add_user(args)

    def get(self):
        return users


class Users(Resource):

    def get(self, user_id):
        result = get_user(user_id)
        if result is not None:
            return result
        else:
            abort(404)

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('user_id')
        parser.add_argument('groups')
        args = parser.parse_args()
        args['user_id'] = user_id
        if valid_record(args) == None:
            return abort(409, message="Malformed data found")
        elif get_user(args['user_id']) is None:
            return abort(404, message="User doesn't exist")
        else:
            delete_user(args['user_id'])
            add_user(args)
        return True

    def delete(self, user_id):
        if get_user(user_id) is None:
            return abort(404, message="User doesn't exist")
        else:
            return delete_user(user_id)

class Groups(Resource):

    def get(self, group_id):
        result = get_group(group_id)
        if result is not None:
            return get_users_in_group(group_id)
        else:
            abort(404, message="Group was not found")

    def delete(self, group_id):
        if get_group(group_id) is None:
            abort(404, message="Specified group does not exist.")
        else:
            return delete_group(group_id)

    def put(self, group_id):
        parser = reqparse.RequestParser()
        parser.add_argument('members')
        args = parser.parse_args()
        try:
            members=json.loads(args['members'])
            if isinstance(members, list)==False:
                return abort(400, message='400 Error: Expected JSON members list.')
        except ValueError:
            return abort(400, message='400 Error: Expected JSON members list.')
        if group_id not in groups:
            return abort(404, message="Group does not exist") 
        return add_group_to_members(group_id, members)
    

class GroupList(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()
        if get_group(args['name']) is not None:
            return abort(409)
        else:
            return add_group(args['name'])

    def get(self):
        return groups

    def put(self, user_id):
        return users[user_id]

api.add_resource(Users, '/users/<string:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(Groups, '/groups/<string:group_id>')
api.add_resource(GroupList, '/groups')
    
if __name__ == "__main__":
    app.run(host= '0.0.0.0',debug=True)
