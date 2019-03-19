#imports needed
import time
import serial
import urllib
import pandas as pd
import numpy as np

#function to read and return value of single thingspeak field
def read_field_thingspeak(channel, api_key, field, results):
    read_link = 'https://api.thingspeak.com/channels/' + str(channel) + '/fields/' + str(field) + '.csv?api_key=' + str(api_key) +'&results=' + str(results)
    df = pd.read_csv(urllib.request.urlopen(read_link))
    df.drop(['created_at'], axis=1, inplace=True)
    return np.array(df)[0][1]

#function that reads thingspeak status
def read_status_thingspeak(channel, api_key, results):
    read_link = 'https://api.thingspeak.com/channels/' + str(channel) + '/status.csv?api_key=' + str(api_key) +'&results=' + str(results)
    return urllib.request.urlopen(read_link)

#function that formats and requests a link to write to two thingspeak fields at once
def write_to_thingspeak(api_key, field1, value1, field2, value2):
    write_link = 'https://api.thingspeak.com/update?api_key=' + str(api_key) + '&field'+ str(field1) +'=' + str(value1) +'&field'+ str(field2) +'=' + str(value2)
    urllib.request.urlopen(write_link)

#function to write status to thingspeak in addtion to both fields
def write_to_thingspeak_status(api_key, field1, value1, field2, value2, status):
    write_link = 'https://api.thingspeak.com/update?api_key=' + str(api_key) + '&field'+ str(field1) +'=' + str(value1) +'&field'+ str(field2) +'=' + str(value2) +'&status=' + status
    urllib.request.urlopen(write_link)

#declare variables related for specific thingspeak channel    
channel = '720608'
read_api_key = 'RRGPJE5YQ8JJPRIR'
write_api_key='C7MKD36DWMJS69UL'

#declare variable for COM port for serial communication
com = '/dev/cu.usbserial-DN051CFK'

#declare variables to validate user input
function_selection = ''
action = ''
print('Fish Feeder Transceiver')
while(function_selection != '0'):
    print('***Main Menu***')
    #prompt user to choose between transmitter or receiver functionality
    function_selection = input('Choose the following:\n1: Transmitter\n2: Receiver\n0: Exit\n')
    if function_selection == '1':
        #while loop that runs for duration of program to prompt for user input
        while(action != '0'):
            #initialization delay to prevent multiple thingspeak write attempts within a short period.
            print('\nInitializing', end='')
            for i in range(15):
                print('.', end='')
                time.sleep(1)
            #prompt user for input and move through program accordingly
            action = input('\n\n***Transmitter***\nChoose the following:\n1: Feed Fish!\n2: Last Time Fish Fed?\n3: Feeder Status\n0: Exit\n')               
            if action == '1':
                #read initial feeder status
                status = read_field_thingspeak(channel,read_api_key,1,1)
                if(status != 0):
                    #if status not empty write the run command to thingspeak
                    write_to_thingspeak(write_api_key,1,1,2,1)
                    #communication delay to ensure time for arduino to process command and respond to thingspeak
                    print('Communicating', end='')
                    for i in range(20):
                        print('.', end='')
                        time.sleep(1)
                
                    #read feeder status to check if feeding was succesful    
                    status = read_field_thingspeak(channel,read_api_key,1,1)
                    if(status==0):
                        print('\nFeeder Empty!')
                        continue
                    elif(status == 1):
                        #read feeder command, if command is still 1 then hardware never read command, if 0 then hardware ran command
                        command = read_field_thingspeak(channel,read_api_key,2,1)
                        if(command == 1):
                            print('\nFeeder Not Responding!')
                        else: 
                            print('\nFood Dispensed.')
                else:
                    #if status is 0 then the feeder is empty
                    print('\nFeeder Empty!')
            elif action == '2':
                #query time last fed and report to user
                df = pd.read_csv(read_status_thingspeak(channel, read_api_key, 1))
                print('Fish last fed', np.array(df)[0][0])
                continue
            elif action == '3':
                #query feeder status and report to user
                #field 1:status(0=EMPTY, 1=READY)
                #field 2:command(0=IDLE, 1=RUN)
                status = read_field_thingspeak(channel,read_api_key,1,1)
                command = read_field_thingspeak(channel,read_api_key,2,1)
                if(status==0):
                    print('Feeder Empty!')
                elif(status==1):
                    print('Feeder Ready.')     
            elif action == '0':
                #terminate program
                print("Transmitter Terminated.")
                break
            else:
                print('Invalid Input!\n\n')
                continue
                
                
    elif function_selection == '2':
        print('***Receiver***')
        try:
            #initialize serial communication
            ser = serial.Serial(com, 9600, timeout=1)
            time.sleep(2)
        except:
            print('Serial Communication Error!\nReturning to Main Menu.\n\n')
        else:
            #while loop that runs while serial communication is open
            while ser.is_open:
    
                #query thingspeak for feeder status and command
                #field 1:status(0=EMPTY, 1=READY)
                #field 2:command(0=IDLE, 1=RUN)
                status = read_field_thingspeak(channel,read_api_key,1,1)
                command = read_field_thingspeak(channel,read_api_key,2,1)
    
                #reset input buffer to ensure latest serial output from board is read
                ser.reset_input_buffer()
                board_status = ser.readline()
    
                #board is communicating empty status
                if(board_status == b'EMPTY\r\n'):
                    if(status!=0):
                        write_to_thingspeak(write_api_key,1,0,2,0)
                        time.sleep(15)
            
                #board is commmunicating ready status
                if(board_status == b'READY\r\n'):
                    #command is IDLE
                    if(command == 0):
                        if(status != 1):
                            write_to_thingspeak(write_api_key,1,1,2,0)
                            time.sleep(15)
                    #command is RUN
                    if(command == 1):
                        ser.write(b'1')
                        time.sleep(15)
                        write_to_thingspeak_status(write_api_key,1,1,2,0,'Food Dispensed')
                #delay    
                time.sleep(1)

            #close serial communication and terminate program
            ser.close()
            print('Serial Communication Closed. Receiver Terminated.')
    elif(function_selection =='0'):
        print('Program Terminated.')
        break
    else:
        print('Invalid Input!\n\n')
        continue
