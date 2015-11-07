import requests

# get a challenge HTTP response
def getResponse( url, dictionary ):

    # send the dictionary at the given location
    response = requests.post( url, json = dictionary );
    
    # reponse is of type Response, parse into JSON form
    response = response.json()

    # access the JSON element
    return response


# register for the challenge, return the userID
def register():

    # create the dictionary to send to the challenge server
    # credentials specified by challenge documentation
    dictionary = { 'email': 'samhinsh@stanford.edu', 
                   'github': 'https://github.com/samhinsh/Code2040Challenge' }

    # send the dictionary at the given location
    userID = getResponse( 'http://challenge.code2040.org/api/register', 
                            dictionary );

    # value specified by the challenge documentation
    userID = userID[ 'result' ]

    print 'You have registered under user ID ' + userID + '!'
    return userID

# reverse a string, return the reversed string to the challenge server

def reverse(token):

    # send the dictionary at the given location
    string = getResponse( 'http://challenge.code2040.org/api/getstring', 
                          token );

    # value specified by the challenge documentation
    string = string[ 'result' ]
    
    # add the "next"-to-last character to a new string
    reversed = ''
    for place in range( 0, len(string) ):
        next = string[ len(string) - 1 - place ]
        reversed += next

    print 'You reversed the string "' + string + '" yielding "' + reversed + '"'
    
    # send reversed string back to the server with user credentials
    token = { 'token': token['token'], 'string': reversed }
    response = getResponse( 'http://challenge.code2040.org/api/validatestring',
                            token );

    print response['result']


# find a needle in a haystack, return its position
def findInHaystack(token):

    payload = getResponse( 'http://challenge.code2040.org/api/haystack', 
                            token )
    print payload

    # needle = payload[ 'needle' ]
    # haystack = payload[ 'haystack' ]

    # print needle
    # print haystack

if __name__ == '__main__':
    
    # register user
    userID = register()

    #create token for future challenges
    token = { 'token': userID }

    # challenges 1-3
    reverse(token)
    findInHaystack(token)

