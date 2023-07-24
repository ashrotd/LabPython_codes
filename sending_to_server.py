import time
from picamera2 import Picamera2
import paramiko
import requests
from bs4 import BeautifulSoup

picam = Picamera2()
camera_config = picam.create_preview_configuration()
picam.configure(camera_config)
capture_interval = 10
output_path = '/home/rd238422/Desktop/Images/'
base_filename = 'image'
image_counter = 1
picam.start()

#configure SSH connection
ssh_host = 'ounppm.eecs.ohio.edu'
ssh_username = 'rdhakal'
ssh_password = 'Ashrot@0775'
remote_directory = '/home/rdhakal/LawnImages/'
while True:
    try:
        filename = output_path + base_filename + str(image_counter)+'.jpg'
        picam.capture_file(filename)
        print(f'Image Captured : {filename}')
        
        #create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host,username=ssh_username,password=ssh_password)
        
        #Create an SFTP client
        sftp = ssh.open_sftp()
        
        #upload to remote server
        sftp.put(filename,remote_directory+base_filename+str(image_counter)+'.jpg')
        print(f'Image Transfered to remote server: {filename}')
        
        
        # Saving target value to remote server
        
        page = requests.get('https://aviationweather.gov/metar/data?ids=KUNI&format=raw&hours=0&taf=off&layout=on')
        soup = BeautifulSoup(page.content,'html.parser')
        data = soup.select("code")
        first10 = data[0]
        
        filename_target = output_path + base_filename + str(image_counter)+'.txt'
        with open(filename_target, 'w') as file:
            file.write(first10.text)
        #for anchor in first10:
            #print(anchor.text)
        sftp.put(filename_target,remote_directory+base_filename+str(image_counter)+'.txt')
        
        #close the SFTP session and SSH connection
        sftp.close()
        ssh.close()
        
        image_counter += 1
        time.sleep(capture_interval)
    except KeyboardInterrupt:
        print("Program halted by user")
        break