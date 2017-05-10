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
    "image": "sesamcommunity/sesam-auth0:latest",
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

The client id and secret are obtained in the Auth0 management console. Remember to give them the users-* scopes.