# Test_Api_Meme
This project contains automated tests for an API that keeps memes. It includes functionality to create, update, delete, and validate memes using Python. The tests verify various aspects of the API, including authentication, meme content verification, and token validation.

Below are the available API endpoints, which allow us to add new memes to the system, modify existing memes, delete them, and, of course, view them.

API Base URL: http://167.172.172.115:52355/

Endpoints
1. POST /authorize
Authorize a user.

Fields:

name (string): The name of the user.
2. GET /authorize/<token>
Check if a token is still valid.

3. GET /meme
Retrieve a list of all memes.

4. GET /meme/<id>
Retrieve a meme by its id.

5. POST /meme
Add a new meme.

Fields (all required):

text (string): The text associated with the meme.
url (string): The URL of the meme image.
tags (array): Tags for categorizing the meme.
info (object): Additional information about the meme.
6. PUT /meme/<id>
Update an existing meme.

Fields (all required):

id (int): The ID of the meme to update.
text (string): Updated text for the meme.
url (string): Updated URL for the meme.
tags (array): Updated tags for the meme.
info (object): Updated additional information about the meme.
7. DELETE /meme/<id>
Delete a meme by its id.

Authorization
All endpoints are available only to authorized users. To make a request as an authorized user, you need to add an Authorization header to your request. The value of this header should be the token obtained from the POST /authorize endpoint.
