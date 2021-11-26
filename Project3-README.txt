Project 3
Team member: Sijie Shang, Danny Ng, Gita Nikzad, and Thomas Eduard Del Rosario

To run this program. Simply use the makefile in the root of the folder. Make will execute the two sql command files in the ./var folder and generate two databases which are named timelines.db and users.db. 
On shell-session, run 'foreman start' to start.

---------------------------------likes.py API--------------------------------
# API calls
**`likePosts(postID, username)`**

> ```shell-session
> $ http POST localhost:5200/likes/ postID=1 username=ProfAvery
> ```

**`likeCount(username)`**

> ```shell-session
> $ http GET localhost:5200/likesCount/ postID=1
> ```

**`likedPosts(username)`**

> ```shell-session
> $ http GET localhost:5200/likedPosts/ username=ProfAvery
> ```

**`topPosts(number)`**

> ```shell-session
> $ http GET localhost:5200/topPosts/ number=3
> ```

> ```---------------------------------polls.py API--------------------------------

In order to run dynamodb:
run the following command in the dynamodb folder
java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar

**`create_polls_table()`**

> ```shell-session
> $ http GET localhost:5300/create_table/
> ```


*`add_items_to_table(username, option1, option2, option3, option4, pollTitle)`**
**`add_items_to_table(username, option1, option2, option3, option4, pollTitle)`**

> ```shell-session
> $ http POST localhost:5300/createPoll/ username=tester option1=apple option2=banana option3=strawberry option4=lemon pollTitle="Favorite fruit?"
> ```


**`get_items_from_table()`**

> ```shell-session
> $ http GET localhost:5300/getAllPost/
> ```

**`vote(option, uservoting, username, pollTitle)`**

> ```shell-session
> $ http POST localhost:5300/vote/ option=apple uservoting=voter username=tester pollTitle="Favorite fruit?"
> ```

**`getPoll(username, pollTitle)`**

> ```shell-session
> $ http GET localhost:5300/getPoll/ username=tester pollTitle="Favorite fruit?"
> ```


**`delete_item(username, pollTitle)`**

> ```shell-session
> $ http DELETE localhost:5300/deletepoll/ username=tester pollTitle="Favorite fruit?"
> ```