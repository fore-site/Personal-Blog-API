import requests

register_body = {
    "username": "foresite",
    "email": "ogunsanu007@gmail.com",
    "password": ""
}

login_body = {
    "username": "fores",
    "password": "xxx"
}

update_user_body = {
    "username": "fores",
    # "email": "ogunsanu007@gmail.com",
}

post_body = {
    "title": "Wonderful day",
    "content": "I am Iron man. Edited",
}

comment_body = {
    "content": "This is admin 1's comment."
}

tag_body = {
    "name": "politics"
}

header = {
    "Authorization": "Bearer xxx"
}

refresh_header = {
    "Authorization": "Bearer xxx"
}

# GET A USER
# user_res = requests.get("http://127.0.0.1:5000/users/2")
# user = user_res.json()
# print(user)

# REGISTER 
# users_req = requests.post("http://127.0.0.1:5000/register", json=register_body)
# users_obj = users_req.json()
# print(users_obj)

# LOGIN
# user_login = requests.post("http://127.0.0.1:5000/login", json=login_body)
# user_login_obj = user_login.json()
# print(user_login_obj)

# PROFILE
# user_profile = requests.get("http://127.0.0.1:5000/profile", headers=header)
# user = user_profile.json()
# print(user)

# UPDATE PROFILE
# user_update = requests.patch("http://127.0.0.1:5000/profile", json=update_user_body, headers=header)
# user = user_update.json()
# print(user)

# REFRESH TOKEN
# user_refresh = requests.post("http://127.0.0.1:5000/refresh", headers=refresh_header)
# user = user_refresh.json()
# print(user)

# LOGOUT 
# user_logout = requests.post("http://127.0.0.1:5000/logout", headers=header)
# user = user_logout.json()
# print(user)

# DEACTIVATE ACCOUNT
# user_del = requests.patch("http://127.0.0.1:5000/profile/deactivate", headers=header)
# user = user_del.json()
# print(user)

# GET POST(S)
# all_posts = requests.get("http://127.0.0.1:5000/posts/4")
# header = all_posts.headers.get('X-Pagination')
# posts = all_posts.json()
# print(posts)
# print(header)

# MAKE A POST
# user_post = requests.post("http://127.0.0.1:5000/posts", json=post_body, headers=header)
# post = user_post.json()
# print(post)

# EDIT A POST
# edit_post = requests.put("http://127.0.0.1:5000/posts/6", json=post_body, headers=header)
# post = edit_post.json()
# print(post)

#DELETE A POST
# delete_post = requests.delete("http://127.0.0.1:5000/posts/4", headers=header)
# delete_post.raise_for_status()
# post = delete_post.json()
# print(post)

# GET POST COMMENTS
# get_post_comment = requests.get("http://127.0.0.1:5000/posts/4/comments")
# header = get_post_comment.headers.get('X-Pagination')
# comments = get_post_comment.json()
# print(comments)
# print(header)

# MAKE COMMENT
# make_comment = requests.post("http://127.0.0.1:5000/posts/4/comments", json=comment_body, headers=header)
# comment = make_comment.json()
# print(comment)

# EDIT COMMENT 
# edit_comment = requests.put("http://127.0.0.1:5000/posts/4/comments/1", json=comment_body, headers=header)
# comment = edit_comment.json()
# print(comment)

# DELETE COMMENT
# delete_comment = requests.delete("http://127.0.0.1:5000/posts/4/comments/1", headers=header)
# comment = delete_comment.json()
# print(comment)

# CREATE TAG
# create_tag = requests.post("http://127.0.0.1:5000/admin/tags", json=tag_body, headers=header)
# tag = create_tag.json()
# print(tag)

# GET TAG(S)
# get_tag = requests.get("http://127.0.0.1:5000/tags/2")
# tag = get_tag.json()
# print(tag)

# LINK TAG AND POST
# link_tag_post = requests.put("http://127.0.0.1:5000/posts/5/tags/2", headers=header)
# tag_post = link_tag_post.json()
# print(tag_post)

# UNLINK TAG AND POST
# unlink_tag_post = requests.delete("http://127.0.0.1:5000/admin/posts/5/tags/2", headers=header)
# tag_post = unlink_tag_post.json()
# print(tag_post)

# GET ALL USERS
# all_users = requests.get("http://127.0.0.1:5000/admin/users", headers=header)
# users = all_users.json()
# print(users)

# SUSPEND USER
# suspend_user = requests.patch("http://127.0.0.1:5000/admin/users/2/suspend", headers=header)
# user = suspend_user.json()
# print(user)

# RESTORE USER
# restore_user = requests.patch("http://127.0.0.1:5000/admin/users/2/restore", headers=header)
# user = restore_user.json()
# print(user)