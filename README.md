Project 2o
Team member: Sijie Shang and Danny Ng

We build a microblogging in this project. We use two separate databases: users.db and timelines.db. The users database stores user information and follower_id and follwing_id. The timelines database stores the username, user_id, posts, and timestamp.


# API calls

**`create_user(username, email, password)`**

> ```shell-session
> $ http POST localhost:8000/users/ username=tester email=test@example.com password=testing bio="This is bio"
> ```

**`authenticateUser(username, password)`**

> ```shell-session
> $ http GET 'localhost:8000/users/?username=ProfAvery&password=password'
> $ http GET localhost:8000/users/ username=ProfAvery password=password

**`addFollower(follower_id, following_id)`**

> ```shell-session
> $ http POST localhost:8000/followers/ follower_id=4 following_id=2
> ```

**`removeFollower(follower_id, following_id)`**

> ```shell-session
> $ http DELETE localhost:8000/followers/ follower_id=4 following_id=2
** `If return 204, then we remove the follower successfully`**

**`getFollowings(user_id)`**

> ```shell-session
> $ http GET localhost:8000/following/ user_id=4
> ```

**`getUserTimeline(username)`**

> ```shell-session
> $ http GET localhost:8000/posts/mypost/ username=ProfAvery
> ```

**`getPublicTimeline()`**

> ```shell-session
> $ http GET localhost:8000/posts/allpost
> ```

**`getHomeTimeline(username)`**

> ```shell-session
> $ http GET localhost:8000/posts/home followings=[2,3]
> ```
**`follwings is a list of following userIDs which can be retreive by using the get following API  `**

**`postTweet(username, text)`**

> ```shell-session
> $ http POST localhost:8000/posts/ username=ProfAvery user_id=1 text='This is a testing post.'
> ```
