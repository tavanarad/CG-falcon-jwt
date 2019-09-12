# CheetaJWT

**CheetaJWT** is a simple module that contains two major classes:

1. JWTHelper
2. JWTMiddleware

These two classes and what they should do will be described by the end of the document.

## JWTHelper
**JWTHelper** is a POPO class that has some method to create, validate JWT Token. Also it should be able to retrieve Playload and Header of the Token. The list of JWTHelper is as below:
1. **encode(playload, secret, algorithm)**
	Creates a JWT token by passing playload.
	
	**Params**

	1. Playload is a dict that contains values that should be added to the token.

	2. Secret is a string that contains value that playload should be encode by it. It can be private key value.

	3. Algorithm is a string that defines the algorithm that should be used to encode the token. If the value of the algorithm is not supported by the pyJWT, the methon should raise an exception that explains the algorithm is not supported.
	
	**Return**

		It should return a JWT token.

2. **decode(token, secret, algorithm)**

	It get token, serect ( may be a public key) and decode algorithm and retrieves the playload.
	
	**Params**

	1. The token is a string that contrains three parts which are splited by dot.
	
	2. The secret is a string that is a phrase that should be used to decode the token. It can be a public key.

	3. Algorithm is a string that defines the algorithm that should be used to encode the token. If the value of the algorithm is not supported by the pyJWT, the methon should raise an exception that explains the algorithm is not supported.
	
	**Returns**

	The decode method should return a dict that contains playload values of the passing token.

## JWTMiddleware
**JWTMiddleware** is a falcon middleware that uses `JWTHelper` to check each incoming request in order to validate the requet's JWT token before processing the resouces. 
If the token is valid, it should pass the playload of the token as named parameter to the particular resouce and named it `jwt_playload` otherwise it should raise a `falcon.HTTPUnauthorized` exception.

### Methods
1. `__init__(options)`

	the constructor of the class get one parameters that contains all options that it needs to use and pass to `JWTHelper` to validate and retrieve JWT Token.
	
	#### Params

	1. **options**
		The options is a dict that contains blew valuse
		1. secret
		2. algorithm
		3. exempt_resources

			it is an array of dicts that each dict contains the name of exempted reousce and exempted method of the resource.

			```python
			exempt_resouces: [
				{
					'name': 'AuthorizationResource',
					'methods': ['OPTIONS', 'GET', 'POST']
				},
				{
					'name': 'UserResource',
					'methods': ['OPTIONS', 'GET']
				},
				{
					'name': 'LogResource',
					'methods': None  # When the methods property is None, it means all methods OPTIONS, GET, POST, PUT, DELETE.
				}
			]
			```

        4. exempt_all_methods
        
            It is an array of method's name that should not be checked for all resources.
            
        5. validators
        
            It's an array of callable methods for validate payload after decode (NOTE: deepcopy of payload will pass to validators so validators can't modify payload)
