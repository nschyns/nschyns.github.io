import sys
import time
import radkit_client

#We make sure we have all the arguments
leng=len(sys.argv)
if(leng==1):
    print("Please add your CCO ID and WLC name as arguments")
else:
    if(leng==2):
        print("Please add your WLC name as argument")
    else:
        print("CCO ID entered:" + sys.argv[1])
        print("WLC name :" + sys.argv[2])
        #We connect to the service
        client=radkit_client.sso_login(sys.argv[1])
        service=client.service("mk9h-kku8-p35k")
        service.update_inventory().wait()
        device=service.inventory[sys.argv[2]]


        output1=device.exec("show run | i country").wait()
        if("wireless country" in output1.result.data):
            print(output1.result.data)
        else:
            print("This WLC is still in wizard mode")
            output2=device.exec("config terminal").wait()
            #We configure the management interface and a country code. This bypasses the day0 wizard
            output3=device.exec("wireless management interface GigabitEthernet1").wait()
            output4=device.exec("wireless country BE").wait()