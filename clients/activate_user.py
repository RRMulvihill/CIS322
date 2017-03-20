import sys
import json

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv)<5 :
        print("Usage: python3 %s <url> <username> <password> <role>"%sys.argv[0])
        return
    
    # Prep the arguments blob
    args = dict()
    args['username']  = sys.argv[2]
    args['password'] = sys.argv[3]
    args['role'] = sys.argv[4]

    # Print a message to let the user know what is being tried
    print("Activating user: %s pass: %s role: %s"%args['username'],args['password'],args['role'])

    # Setup the data to send
    sargs = dict()
    sargs['arguments']=json.dumps(args)
    data = urlencode(sargs)
    print("sending:\n%s"%data)
    
    # Make the resquest
    path = sys.argv[1] + 'create_user'
    req = Request(path,data.encode('ascii'),method='POST')
    res = urlopen(req)
    
    # Parse the response
    resp = json.loads(res.read().decode('ascii'))
    
    # Print the result code
    print("Call to LOST returned: %s"%resp)
    

if __name__=='__main__':
    main()
