from picamera2 import Picamera2
import paramiko
import io
from io import BytesIO
import time
import requests
from bs4 import BeautifulSoup
import datetime


picam = Picamera2()
camera_config = picam.create_preview_configuration()
picam.configure(camera_config)
capture_interval = 1200
output_path = '/home/rd238422/Desktop/Images/'
base_filename = 'image'
image_counter = 1
picam.start()

#configure SSH connection
ssh_host = 'ounppm.eecs.ohio.edu'
ssh_username = 'rdhakal'
ssh_password = 'Ashrot@0775'
remote_directory = '/home/rdhakal/LawnImages/'
output_path = '/home/rd238422/Desktop/Images/'
while True:
    try:
        image_stream = io.BytesIO()
        
        # Capture the image
        picam.capture_file(image_stream,format='jpeg')
        
        # Reset the stream position to the begining
        image_stream.seek(0)
        
        # Scraping the Target values for website
        page = requests.get('https://aviationweather.gov/metar/data?ids=KUNI&format=raw&hours=0&taf=off&layout=on')
        soup = BeautifulSoup(page.content,'html.parser')
        data = soup.select("code")
        first_data = data[0].text
        data_byte = first_data.encode('utf-8')
        
        # Write locally
        #with open(output_path+base_filename+str(image_counter)+'.jpg','wb') as file:
           # file.write(image_stream.getvalue())
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host,username=ssh_username,password=ssh_password)
        
        #Create an SFTP client
        sftp = ssh.open_sftp()
        
        #Set the current time and date
        current_time = datetime.datetime.now().strftime('%Y%m%d_%H_%M')
        
        # Upload the image stream to the remote server
        remote_image_path = remote_directory+current_time+base_filename+ str(image_counter)+'.jpg'
        sftp.putfo(image_stream,remote_image_path)
        
        # Upload the target txt value to remote server
        file_object = BytesIO(data_byte)
        remote_file = remote_directory+current_time+"METAR"+str(image_counter)+'.txt'
        sftp.putfo(file_object,remote_file)
        # Close the SFTP session and SSH Connection
        sftp.close()
        ssh.close()
        
        image_counter += 1
        time.sleep(capture_interval)
    except KeyboardInterrupt:
        print("Program halted by user")
        break
        
