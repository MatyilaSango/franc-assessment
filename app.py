from flask import Flask, render_template, jsonify, Response, request, redirect
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    newUser = request.args.get('new-user')
    newPost = request.args.get('new-post')

    #Viewing user's timeline
    if (type(username) != type(None)) and (type(newUser) == type(None)) and (type(newPost) == type(None)):

        #getting friends
        with open('./users.json', 'r') as f:
            users = f.read()

        #converting json to python object
        py_friends = json.loads(users)

        #extracting user's posts
        user_friends = py_friends[username]


        #get posts
        with open('./posts.json', 'r') as f:
            posts = f.read()

        #converting json to python object
        py_tweets = json.loads(posts)

        #extracting user's posts
        user_posts = py_tweets[username]

        #Adding friends posts in users timeline
        for user_ in user_friends:
            for user_s_post in py_tweets[user_]:
                user_posts.append(user_s_post)

        #sorting the posts chronologically using bubble sort
        for i in range(len(user_posts)-1):
            for j in range(len(user_posts)-i-1):
                if( datetime.strptime(user_posts[j]["time"], "%Y-%m-%dT%H:%M:%SZ") > datetime.strptime(user_posts[j+1]["time"], "%Y-%m-%dT%H:%M:%SZ")):
                    temp = user_posts[j]
                    user_posts[j] = user_posts[j+1]
                    user_posts[j+1] = temp

        #converting python object into json
        json_tweets = json.dumps(user_posts)

        #converting python object into json
        json_friends = json.dumps(user_friends)

        return render_template('index.html', username = username, tweets = json_tweets, friends = json_friends)

    #Loading home page with user accounts
    elif (type(username) == type(None)) and (type(newUser) == type(None)) and (type(newPost) == type(None)):

        #getting users
        with open('./users.json', 'r') as f:
            users = f.read()

        #converting json to python object
        py_users = json.loads(users)

        #getting user list
        user_list = list(py_users.keys())

        #converting python object into json
        list_users = json.dumps(user_list)

        return render_template('index.html', username = username, users = list_users)

    #Adding a new user
    elif (type(username) == type(None)) and (type(newUser) != type(None)) and (type(newPost) == type(None)):

        #getting users
        with open('./users.json', 'r') as f:
            users = f.read()

        #converting json to python object
        py_users = json.loads(users)

        #adding account
        py_users[newUser] = []

        #converting python object into json
        list_users = json.dumps(py_users)

        #Saving list of users
        with open('./users.json', 'w') as f:
            f.write(list_users)


        #get posts
        with open('./posts.json', 'r') as f:
            posts = f.read()

        #converting json to python object
        py_tweets = json.loads(posts)

        #adding an empy posts
        py_tweets[newUser] = []

        #converting python object into json
        json_tweets = json.dumps(py_tweets)

        #Saving posts
        with open('./posts.json', 'w') as f:
            f.write(json_tweets)

        newUser = None

        return redirect('/')

    #Adding a new post
    elif (type(username) != type(None)) and (type(newUser) == type(None)) and (type(newPost) != type(None)):

        #get posts
        with open('./posts.json', 'r') as f:
            posts = f.read()

        #converting json to python object
        py_tweets = json.loads(posts)

        #extracting user's posts
        user_posts = py_tweets[username]

        #creating new post
        new_post = {
            "status": newPost,
            "time": str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
        }

        #adding new post in user's post list
        user_posts.append(new_post)

        #adding user's posts in post list
        py_tweets[username] = user_posts

        #converting python object into json
        json_tweets = json.dumps(py_tweets)


        #Saving posts
        with open('./posts.json', 'w') as f:
            f.write(json_tweets)

        newPost = None

        return redirect('/?username='+username)


@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='127.0.0.1')