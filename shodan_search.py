import shodan # this is important believe it or not
import csv # needed for writing to csv 
import json # for dumping them dicts to the filez

shodan_key = open("keyfile.txt","r") # fetch your own key from your text file
api = shodan.Shodan(shodan_key) # now we can use shodan module to search with the shodan_key


# First stage is asking the user what they want to search
# This will be dicated by the setup() function
# When a user specifies, the relevant function is called from the console 
execute = input("""


1. ipsrch - enrich a specific IP address
2. pipsrch - enrich a specific IP and print
3. freesrch - search for services or general strings
4. pfreesrch - print results from searching general services
5. shutdown - stops the program

Please enter your command here: """)



# This free search functions let you look for stuff like "apache"
# Needs to be edited to print to files but also to make more complex searches

def free_search():

  try:

    # Search Shodan
    input_entered = input("Enter string to search: ")
    results = api.search(input_entered)

    # Show results
    print("Results found: {}".format(results["total"]))

    # Iterate through each result and print our contents from the dictionary
    for result in results["matches"]:
        print("IP: {}".format(result["ip_str"]))
        print(result["data"])
        print("")
  except shodan.APIError:
        print("Search error")
        return setup()


# This IP search is to enrich specific IP addresses
# Needs editing to potentially add more contents
# Needs something to support addition of multiple IP addresses
# Needs to be able to print to a file such as CSV 

def ip_search():

  try:

    # Search Shodan for IP address

    input_ip = input("Enter an IP address: ")
    host = api.host(input_ip)

    # Print general info

    print("""
            IP:{}
            Organization: {}
            Operating System: {}
            
          """.format(host["ip_str"], host.get("org", "n/a"), host.get("os", "n/a")))

    # Print all banners

    for item in host['data']:
      print("""
                Port: {}
                Banner: {}

        """.format(item['port'], item['data']))
      
  except shodan.APIError: # basically if it breaks we get an error 
    print("Search error")
    return setup()



def pip_search():

  try:

    # Search Shodan for IP address

    input_ip = input("Enter an IP address to enrich: ")
    host = api.host(input_ip)

    # Print general info

    print("""
            IP:{}
            Organization: {}
            Operating System: {}
            
          """.format(host["ip_str"], host.get("org", "n/a"), host.get("os", "n/a")))

    # Iterate through and put it in a doc

    with open('pip_search-%s.txt' % (input_ip),'w') as f1:
      for item in host['data']:
        f1.write("""
        Host: {}
        Organization: {}
        Operating System: {}
        Port: {}
        Banner: {}
        """.format(host["ip_str"],host.get("org","N/A"), host.get("os","N/A"), item['port'], item['data']))
        
    f1.close()
        
            
  except shodan.APIError: # basically if it breaks we get an error 
    print("Search error")
    return setup()

# Setup function to allow user to dictate which one will be called
# Whatever is entered into input will dictate this part  
def setup():

  if execute == "freesrch":
    return free_search()
  elif execute == "ipsrch":
    return ip_search()
  elif execute == "pipsrch":
    return pip_search()
  elif execute == "pfreesrch":
    return pfree_search()
  else:
    print("You have not entered a recognized command")
  


setup()