# Simple Social Backend

Frontend: https://github.com/53kyle/sm-frontend

Simple Social uses Django for its backend and database. In production, this is running on an AWS EC2 server. Images are stored along with the frontend on an AWS S3 bucket, and are cached via an AWS CloudFront distribution.

## Required Packages
- django-cors-headers
- djangorestframework
- django-storages
- Pillow
- boto3

## Implemented Endpoints
- 'register/': POST only. Used for registering new users.
- 'login/': POST only. Used for securely logging in via username and password.
- 'logout/': POST only. Used for logging the user out.
- 'users/': GET only. Used for fetching a list of all user objects.
- 'users/[USERNAME]/': GET only. Used for fetching a specific user object.
- 'users/[USERNAME]/profile-pic/': GET and POST. Used for fetching the path to an existing user's profile pic, and for uploading an image as a user's profile pic.
- 'users/[USERNAME]/follows/': GET and POST. Used for fetching a list of users which a given user follows, or for flagging that a given user follows another.
- 'users/[USERNAME]/follows/[OTHER_USERNAME]/': GET only. Used to determine whether a user follows another.
- 'users/[USERNAME]/followers/': GET and POST. Used for fetching a list of users which follow a given user, or for flagging that a given user follows another.
- 'users/[USERNAME]/followers/[OTHER_USERNAME]/': GET only. Used to determine whether a user is followed by another.
- 'posts/': GET and POST. Used for fetching the 10 most recent post objects globally, and for adding a new post object.
- 'posts/after/[LATEST_DATETIME]/': GET only. Used for fetching the 10 most recent posts which were posted prior to 'LATEST_DATETIME'.
- 'posts/following/[USERNAME]/': GET only. Used for fetching the 10 most recent post objects, which were posted by users that 'USERNAME' follows.
- 'posts/following/[USERNAME]/after/[LATEST_DATETIME]/': GET only. Used for fetching the 10 most recent post objects, which were posted by users that 'USERNAME' follows, and which were posted prior to 'LATEST_DATETIME'.
- 'posts/[POST_ID]/': GET only. Used for fetching a specific post object.
- 'posts/[POST_ID]/replies/': GET and POST. Used for fetching the 10 most recent post objects which are replies to another post, and for adding a new post object which is a reply to another post.
- 'posts/[POST_ID]/replies/after/[LATEST_DATETIME]/': GET only. Used for fetching the 10 most recent post objects, which are replies to another post, and which were posted prior to 'LATEST_DATETIME'.
- 'users/[USERNAME]/posts/': GET only. Used for fetching the 10 most recent post objects which were posted by 'USERNAME'.
- 'posts/[USERNAME]/posts/after/[LATEST_DATETIME]/': GET only. Used for fetching the 10 most recent post objects, which were posted by 'USERNAME', and which were posted prior to 'LATEST_DATETIME'.
- 'posts/[PARENT_POST_ID]/likes/': GET and POST. Used for fetching the numebr of likes on a given post, and for adding a like to a given post.
- 'posts/[PARENT_POST_ID]/likes/[USERNAME]/': GET only. Used to determine whether 'USERNAME' liked a given post.
- 'posts/[PARENT_POST_ID]/dislikes/': GET and POST. Used for fetching the numebr of dislikes on a given post, and for adding a dislike to a given post.
- 'posts/[PARENT_POST_ID]/dislikes/[USERNAME]/': GET only. Used to determine whether 'USERNAME' disliked a given post.
- 'search/users/[SEARCH_TERM]/: GET only. Fetches a list of users with a username containing 'SEARCH_TERM'.
- 'search/posts/[SEARCH_TERM]/: GET only. Fetches post objects with contents containing 'SEARCH_TERM'.

## Implemented Models
- 'SM_User' - Consists of username, email, password, and bio.
- 'Profile_Pic' - Consists of username and path-to-image.
- 'Follow' - Consists of two usernames, the follower and the followee.
- 'Post' - Consists of username (poster), contents, date/time posted, and the post id of the post it's replying to (if any).
- 'Post_Like' - Consists of username and post id.
- 'Post_Dislike' - Consists of username and post id.
