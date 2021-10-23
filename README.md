Project 2
Team member: Sijie Shang and Danny Ng

To run this program. Simply use the makefile in the root of the folder. Make will execute the two sql command files in the ./var folder and generate two databases which are named timelines.db and users.db. 
On shell-session, run 'foreman start -m users=1,timelines=3' to start all instances with gUnicorn. 

All APIs can be test with httpie bu using the following examples.

Timelines service is running 3 instances with HAProxy load banancing the workload. All endpoints traffics are redirected to 127.0.0.1:80. While the Users service is running on its owe because no load balancing is needed in our case. 

We build a microblogging in this project. We use two separate databases: users.db and timelines.db. The users database stores user information and follower_id and follwing_id. The timelines database stores the username, user_id, posts, and timestamp.


# API calls

**`create_user(username, email, password)`**

> ```shell-session
> $ http POST localhost:5000/users/ username=tester email=test@example.com password=testing bio="This is bio"
> ```

**`authenticateUser(username, password)`**

> ```shell-session
> $ http GET 'localhost:5000/users/?username=ProfAvery&password=password'
> $ http GET localhost:5000/users/ username=ProfAvery password=password

**`addFollower(follower_id, following_id)`**

> ```shell-session
> $ http POST localhost:5000/followers/ follower_id=4 following_id=2
> ```

**`removeFollower(follower_id, following_id)`**

> ```shell-session
> $ http DELETE localhost:5000/followers/ follower_id=4 following_id=2
** `If return 204, then we remove the follower successfully`**

**`getFollowings(user_id)`**

> ```shell-session
> $ http GET localhost:5000/following/ user_id=4
> ```

**`getUserTimeline(username)`**

> ```shell-session
> $ http GET localhost/posts/mypost/ username=ProfAvery
> ```

**`getPublicTimeline()`**

> ```shell-session
> $ http GET localhost/posts/allpost
> ```

**`getHomeTimeline(username)`**

> ```shell-session
> $ http GET localhost/posts/home followings=[2,3]
> ```
**`follwings is a list of following userIDs which can be retreive by using the get following API  `**

**`postTweet(username, text)`**

> ```shell-session
> $ http POST localhost/posts/ username=ProfAvery user_id=1 text='This is a testing post.'
> ```


**`Config file for haProxy`**

> ```shell-session
> $ sudo nano /etc/haproxy/haproxy.cfg
> ```

frontend http_front
   bind *:80
   stats uri /haproxy?stats
   default_backend http_back

backend http_back
   balance roundrobin
   server timelines1 127.0.0.1:5100 check
   server timelines2 127.0.0.1:5101 check
   server timelines3 127.0.0.1:5102 check

**`To start HAProxy, use following command`**
 **sudo /etc/init.d/haproxy start
