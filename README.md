[![E+E_Logo](./images/epluse-logo.png)](https://www.epluse.com/en/)

# HTM502 I2C with Raspberry Pi 


![HTM502](./images/HTM502.png) 


<!--[![button1](./images/learn-more.png)](https://www.epluse.com/products/humidity-instruments/humidity-sensing-elements/htm502/)   -->
[![button2](./images/data-sheet.png)](https://www.epluse.com/fileadmin/data/product/htm502/datasheet_HTM502.pdf) 



## QUICK START GUIDE  

### Components 
- HTM502
- Raspberry Pi 4
- Breadboard 
- Wire jumper cable <br>

| Step |                                                                                                                                                             |
|------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1    | Connect the HTM502 sensor module with Raspberry Pi according to the following scheme:<br>[<img src="images/HTM502_rpi.png" width="50%"/>](images/HTM502_rpi.png)|
| 2    | Download and install the operating system (https://www.raspberrypi.org/software/operating-systems/).                                                            |
| 3    | Boot Raspberry Pi and complete any first-time setup if necessary (find instructions online).                                                                |
| 4    | Activate I2C communication:https://github.com/fivdi/i2c-bus/blob/master/doc/raspberry-pi-i2c.md                     |
| 5    | Download and install the "smbus2" library on the Raspberry Pi. [Instruction](https://pypi.org/project/smbus2/#:~:text=Installation%20instructions)            |
| 6    | Clone the repository: ```git clone https://github.com/epluse/HTM502_i2c_rpi.git```  |
| 7    | Open a command shell and type following command to receive measurement data – that’s it! |


### Example output

```shell
pi@raspberrypi:~ $ python3 HTM502_i2c_single_shot.py
	temperature , relative humidity
	23.41 °C , 50.64 %RH 
```
<br>
<br>

## License 
See [LICENSE](LICENSE).
