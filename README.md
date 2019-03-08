README
======
Flask app to implement API that keeps users and their group membership.

# Getting the image
```
docker pull docker.io/faridsaad/users:v1
```

# Running it
```
docker run --rm -it -p 5000:5000 users:v1
```

# Example requests:
### Get all users:
```
curl -X GET localhost:5000/users
```

### Get details on user
```
curl -X GET  localhost:5000/users/fsaad
```

### Create new user
```
curl -X POST -d "first_name=some" -d "last_name=user" -d "user_id=someid" -d "groups=''" localhost:5000/users
```

### Delete user:
```
curl -X DELETE localhost:5000/users/someid
```

### Adding user to admins group example:
```
curl -X PUT -d 'members=["fsaad"]' localhost:5000/groups/admins
```

### Get admins group membership:
```
curl -X GET localhost:5000/groups/admins
```

### Add users to a group:
```
curl -X PUT -d 'members=["user1","user2"]' localhost:5000/groups/dev
```

### Delete a group:
```
curl -X DELETE localhost:5000/groups/dev
```
