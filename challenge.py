import requests

# get a challenge HTTP response

def getResponse( url, dictionary ):

    # send the dictionary at the given location
    response = requests.post( url, json = dictionary );
    
    # reponse is of type Response, parse into JSON form
    response = response.json()

    # access the payload of the JSON element, speficied 
    # by the challange documentation
    return response['result']


# register for the challenge, return the userID

def register():

    # create the dictionary to send to the challenge server
    # credentials specified by challenge documentation
    dictionary = { 'email': 'samhinsh@stanford.edu', 
                   'github': 'https://github.com/samhinsh/Code2040Challenge' }

    # send the dictionary at the given location
    userID = getResponse( 'http://challenge.code2040.org/api/register', 
                            dictionary );

    print 'You have registered under user ID ' + userID + '!'
    return userID

# reverse a string, return the reversed string to the challenge server

def reverse(token):

    # send the dictionary at the given location
    string = getResponse( 'http://challenge.code2040.org/api/getstring', 
                          token );
    
    # add the "next"-to-last character to a new string
    reversed = ''
    for place in range( 0, len(string) ):
        next = string[ len(string) - 1 - place ]
        reversed += next

    print 'You reversed the string "' + string + '" yielding "' + reversed + '"'
    
    # send reversed string back to the server with user credentials
    token = { 'token': token['token'], 'string': reversed }
    success = getResponse( 'http://challenge.code2040.org/api/validatestring',
                            token );

    print success



# find a needle in a haystack, return its position to the challenge server

def findInHaystack(token):

    payload = getResponse( 'http://challenge.code2040.org/api/haystack', 
                            token )

    # singleton element
    needle = payload[ 'needle' ]

    # array element
    haystack = payload[ 'haystack' ]

    # position in the array
    position = -1

    counter = 0
    for element in haystack:
        if element == needle:
            position = counter
            break
        counter += 1

    print "Needle found at position " + str(position) + " in haystack"

    # send result to challenge server
    token = { 'token': token['token'], 'needle': position }
    success = getResponse( 'http://challenge.code2040.org/api/validateneedle',
                            token );

    print success

# Returns an array containing only strings without the prefix to the challenger server

def removePrefixes(token):

    payload = getResponse( 'http://challenge.code2040.org/api/prefix', 
                           token );
    print payload
    prefix = payload[ 'prefix' ]
    array = payload[ 'array' ]

    # filter all strings from the array not starting with the prefix
    array = filter(lambda str: str[ 0 : len(prefix) ] != prefix, array )

    for word in array:
        print word

    # manually parse JSON, 'result' is not a key in this response 
    # send the results to the challenge server
    token = { 'token': token['token'], 'array': array }

    # send the dictionary at the given location
    response = requests.post( 'http://challenge.code2040.org/api/validateprefix', 
        json = token );
    
    # reponse is of type Response, parse into JSON form
    response = response.json()

    print response

if __name__ == '__main__':
    
    # register user
    userID = register()

    # create login token for challenges
    token = { 'token': userID }

    # Stages I-IV
    reverse(token)
    findInHaystack(token)
    removePrefixes(token)
