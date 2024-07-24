# Precision Landing System for Drones

## Requirements
- Python 3.8.10
- [ultralytics/yolov5](https://github.com/ultralytics/yolov5)
- Dronekit 2.9.2 
- Mavproxy 1.8.46
- PyMavlink 2.4.8

## Installation
1. Clone the repository
```bash
git clone https://github.com/abinashlingank/AeroGaze.git
```

2. Install the required packages
```bash
pip install -r requirements.txt
```
3. Change the constants in the Constants.py file
    - ` connectionString = '<IP_Address>:14550'  # Connection String `
        where `<IP_Address>` is the IP address of the drone.



### Example MavProxy command to connect to the drone:
```bash
mavproxy.py --master tcp:<IP_Address>:5760 --out <IP_Address>:14550 --out <IP_Address>:14551
```

> [!NOTE]
> Instead of running the mavproxy command, edit the 'run' file in the root folder and replace the IP address with the IP address of the drone.


---

- Need to give permission in Raspberry pi to access the serial port
```bash
sudo usermod -a -G dialout $USER
```

### Params

**PILOT_THR_BHV = 4**
This parameter enables to arm the drone with the program




