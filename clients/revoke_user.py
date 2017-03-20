import sys

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv) != 3 :
        print("Usage: python3 %s <url> <username>"%sys.argv[0])
        sys.exit()
    
    # Prep the arguments
    args = dict()
    args['username']  = sys.argv[2]

    print("Revoking user: %s"%args['username'])

    data = urlencode(args)
    
    # Make the resquest
    path = sys.argv[1] + 'revoke_user'
    req = Request(path,data.encode('ascii'),method='POST')
    res = urlopen(req)
    
    # Print the result code
    print(res.read().decode('ascii'))
    

if __name__=='__main__':
    main()
    
