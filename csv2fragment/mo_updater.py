import csv,sys,getopt,requests

# Requirements:
#  - network connection maybe http-proxy config
#  - credentials on CoT (upper/lower-case od username is important
#  - CSV-File with the following syntax:
#  - Python > 2.8
#  - Installed Module "requests" on Python
#
# ---start file-------
#        Device ID,Client ID,Client Email
#        695132,BRUN 6,BRUN6@vet.com
#        1970611,ASSM 1,ASSM1@vet.com
#        1970612,HAMJ 6,HAMJ6@vet.com
# --- end file -------
#
# Example of call of python script:
#     mo_updater.py clientdetails.csv  https://sometenanturl.ram.m2m.telekom.com  yvobogers@someserver.com somepassword

def postRequest(urlname,username,password,deviceid,clientid,email):
    print (f'Posting request for updating MO of [deviceid={deviceid},clientid={clientid},email={email}] on [{urlname}]...')
    newurl = urlname+'/inventory/managedObjects/'+deviceid
    print (f'url={newurl}')
    data = '{ "custom_config": { "customerEmail": "'+email+'", "customerId": "'+clientid+'" } }"'
    response = requests.put(url = newurl, data = data, auth=(username, password)) 
    print (f'PUT-Response={response}')
    print (f'POST-Request finished.')

def main(argv):
   if len(sys.argv) != 5:
      print (sys.argv[0], '<csvfile> <url> <username> <password>')
      sys.exit(2)

   csvfile = sys.argv[1]
   url = sys.argv[2]
   username = sys.argv[3]
   password = sys.argv[4]
         
   print (f'Csvfile is "{csvfile}"')
   print (f'Url is "{url}"')
   print (f'Username is "{username}"')

   deviceid = ''
   clientid = ''
   email = ''
   
   with open(csvfile) as csv_file:
       csv_reader = csv.reader(csv_file, delimiter=',')
       line_count = -1
       for row in csv_reader:
           if line_count == -1:
               # First line is header. Ignore it.
               line_count += 1
           else:
               deviceid = row[0]
               clientid = row[1]
               email = row[2]     
               postRequest(url,username,password,deviceid,clientid,email)
               line_count += 1
       print(f'Processed {line_count} devices.')

if __name__ == "__main__":
   main(sys.argv[1:])
   

