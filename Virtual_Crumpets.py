def status(usr_port):
    """
The status function is used to recieve the requested user input from the light function and output the desired status code to the Arduino board.

The status function requires that you set the communication serial port that the hardware is plugged into. Go to your Hardware section of your computer to determine the correct port and enter the port number only. i.e... if the port is COM2, enter 2 into the status function.

The command should be:

        *status(2)    * Make sure to replace the 2 with the specific COM port your computer is using or this function will not do as intended.
    """
    # Imports
    import requests
    import serial
    import time
    # Build url for downloading to ThingSpeak
    base_url = 'https://api.thingspeak.com/channels/714178/fields/1.json?api_key='
    key='O8UW05CXGWM34FYV'
    mid_url = '&results'
    end_url = '='
    results_num = '1'
    url = base_url+key+mid_url+end_url+results_num
    # Open Serial Port
    ser = serial.Serial(f'COM{usr_port}',9600)
    # Download Data and apply the "data" to the light * data = 0(light off), data = 1(light on) and data>1(light off and reset serial)
    r = requests.get(url)
    json_data = r.json()
    data = int(json_data['feeds'][0]['field1'])
    if data == 1:
        time.sleep(2)
        ser.write(b'N')
        print('The light is currently on!')
        init_data=1
    elif data == 0:
        time.sleep(2)
        ser.write(b'F')
        print('The light is currently off!')
        init_data=0
    elif data>1:
        time.sleep(2)
        ser.write(b'F')
        print('The light is currently off!')
        init_data=3
    # Start a "while" loop to continuously scan for changes in the data then apply that change to the light
    while not (data>=5):
        r = requests.get(url)
        json_data = r.json()
        curr_data=int(json_data['feeds'][0]['field1'])
        # If curr_data and init_data are the same (on or off request hasn't changed) then look again until it does change
        if curr_data==init_data:
            pass
        elif curr_data == 1:
            time.sleep(2)
            ser.write(b'N')
            print('Your request has been processed and the light is now on!')
            init_data=1
        elif curr_data == 0:
            time.sleep(2)
            ser.write(b'F')
            print('Your request has been processed and the light is now off!')
            init_data=0
        elif curr_data>1:
            time.sleep(2)
            ser.write(b'F')
            ser.close()
            time.sleep(10)
            r = requests.get('https://api.thingspeak.com/update?api_key=C20UYZD60U7HNPRJ&field1=0')
            json_data = r.json()
            break
    print('To recieve external requests, please restart the status() function')
    return
            
def light():
    """
The light function receives an ```on``` or ```off``` command from the user and submits the request to ThingSpeak to switch the hardware to the desired status.
Simply include the desired status:

        *light(on) or light(ON) or light(On)
        
        *light(off) or light(OFF) or light(Off)
        
        *light(quit) or light(Quit) or light(Q) or light(q)
        
    The request will be output to ThingSpeak and must be received on the outlet side before functionality will be present. To receive the request, use the ``status(usr_port)`` function
    """
    # Start a "while" loop to ask for user input continuously until a quit command is entered
    while True:
        # Imports
        import time
        # Ask for input from the user
        usr_cmd=input('Would you like the light "On" or "Off" or do you want to "Quit"? ')
        # Insert delay of request for minimal website error
        time.sleep(10)
        # Start a "while" loop for error checking purposes
        while not (usr_cmd=='on' or usr_cmd=='On' or usr_cmd=='ON' or usr_cmd=='off' or usr_cmd=='Off' or usr_cmd=='OFF' or usr_cmd=='Quit' or usr_cmd=='Q' or usr_cmd=='q' or usr_cmd=='quit'):
            usr_cmd=input('You must select on, off or quit! ')
        # Imports
        import requests
        # Build url for uploading user request to website
        base_url = 'https://api.thingspeak.com/update?api_key='
        mid_url = '&field1='
        code='C20UYZD60U7HNPRJ'
        if usr_cmd=='on' or usr_cmd=='On' or usr_cmd=='ON':
            on_off = '1'
            url = base_url+code+mid_url+on_off
            r = requests.get(url)
            json_data = r.json()
            print('Must have been too dark for you!')
        elif usr_cmd=='off' or usr_cmd=='Off' or usr_cmd=='OFF':
            on_off = '0'
            url = base_url+code+mid_url+on_off
            r = requests.get(url)
            json_data = r.json()
            print("Ok, but the dark scares me!")
        elif usr_cmd=='Quit' or usr_cmd=='Q' or usr_cmd=='q' or usr_cmd=='quit':
            on_off = '3'
            url = base_url+code+mid_url+on_off
            r = requests.get(url)
            json_data = r.json()
            print("You have removed your capability to choose and it must be restarted at the hardware!")
            break