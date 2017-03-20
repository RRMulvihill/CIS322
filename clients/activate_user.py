import sys
import json

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

main()
    # Check the CLI arguments
    if len(sys.argv) !=5 :
        print("Usage: python3 %s <url> <username> <password> <role>"%sys.argv[0])
        sys.exit()
    
    # Prep the arguments blob
    args = dict()
    args['username']  = sys.argv[2]
    args['password'] = sys.argv[3]
    
    #get role
    if (sys.argv[4] != 'logofc' and sys.argv[4] != 'facofc'):
        print("role must be either 'logofc' or 'facofc'")
        sys.exit()
    if sys.argv[4] == 'logofc':
        args['role'] = 1
    if sys.argv[4] == 'facofc':
        args['role'] = 2
    
    data = urlencode(args)

    # Print a message to let the user know what is being tried
    print("Activating user: %s pass: %s role: %s"%args['username'],args['password'],args['role'])
    
    # Make the resquest
    path = sys.argv[1] + 'activate_user'
    req = Request(path,data.encode('ascii'),method='POST')
    res = urlopen(req)
    
    # Print the result code
    print(res.read().decode('ascii'))
    

if __name__=='__main__':
    main()
