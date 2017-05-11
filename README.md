# sesam-auth0
Reads and writes users to Auth0.

## sources

An example of system config: 

```json
[{
  "_id": "my-auth0",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "DOMAIN": "my-auth0.eu.auth0.com",
      "NON_INTERACTIVE_CLIENT_ID": "...",
      "NON_INTERACTIVE_CLIENT_SECRET": "..."
    },
    "image": "sesamcommunity/auth0:latest",
    "port": 5000
  }
},
{
  "_id": "read-auth0-users",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "my-auth0",
    "supports_since": true,
    "url": "/users?batch_size=50"
  }
}]
```

## sinks

You can update users. Auth0 behaves a bit strange when creating users. If you create a user with an email/sms/etc, the existing user will be updated (but will get a new invite email, etc.) instead of a new one created. Also Auth0 will assign a user id to new users, and the only way to update the email/sms/etc or delete the user is to pass in the generated id.

Also the auth0 api will not reflect the updates immediately, so you might not see the recently created or updated user in the source.

If you need to delete and update users the flow must be that you grab the users using the source, merge them with you customers based on something stable (e.g. a reference as user metadata) and that you assign the auth0 id as ``_id`` when you send them to the sink.

The client id and secret are obtained in the Auth0 management console. Remember to give them the users-* scopes.
