import requests

def register():

    # create the dictionary to send to the challenge server
    # credentials specified by challenge documentation
    dictionary = { 'email': 'samhinsh@stanford.edu', 
                   'github': 'https://github.com/samhinsh/Code2040Challenge' }

    # send the dictionary at the given location
    response = requests.post( "http://challenge.code2040.org/api/register", 
                              json = dictionary );

    # reponse is of type Response, parse into JSON form
    response = response.json()
    
    # access the element as described in the challenge documentation
    user = response['result']

    return user

if __name__ == '__main__':
    user = register()
    print "You have registered under user ID " + user + "!"

