import requests
import iso8601
from datetime import timedelta

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

    # send result to challenge server
    token = { 'token': token['token'], 'needle': position }
    success = getResponse( 'http://challenge.code2040.org/api/validateneedle',
                            token );

    print success

# Returns an array containing only strings without the prefix, to the challenge server

def removePrefixes(token):

    payload = getResponse( 'http://challenge.code2040.org/api/prefix', 
                           token );
    prefix = payload[ 'prefix' ]
    array = payload[ 'array' ]

    # filter all strings not starting with the prefix from the array 
    array = filter(lambda str: str[ 0 : len(prefix) ] != prefix, array )

    # send filtered array string back to the server with user credentials
    token = { 'token': token['token'], 'array': array }
    success = getResponse( 'http://challenge.code2040.org/api/validateprefix',
                            token );

    print success

# plays the dating game and returns the new date to the challenge server

def datingGame(token):

    payload = getResponse( 'http://challenge.code2040.org/api/time', 
                           token );

    datestamp = payload[ 'datestamp' ]
    interval = payload[ 'interval']

    # parse the iso8601 timestamp into a datetime timestamp
    datestamp = iso8601.parse_date(datestamp)

    # convert time interval to a datetime timestamp
    interval = timedelta( seconds = interval )

    # add the two timestamps together
    datestamp = datestamp + interval

    # convert new timestamp to iso8601
    datestamp = datestamp.isoformat()

    # send updated time string back to the server with user credentials
    token = { 'token': token['token'], 'datestamp': datestamp }
    success = getResponse( 'http://challenge.code2040.org/api/validatetime',
                            token );

    print success

if __name__ == '__main__':
    
    # register user
    userID = register()

    # create login token for challenges
    token = { 'token': userID }

    # Stages I-IV
    reverse(token)
    findInHaystack(token)
    removePrefixes(token)
    datingGame(token)
