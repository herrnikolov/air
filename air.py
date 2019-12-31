#!/usr/bin/env python
import requests
from lxml import html
from time import sleep
from lcdproc.server import Server

def main():
    #Variables
    lcd_proc_server = "127.0.0.1"
    air_station = 'http://127.0.0.1/values'
    measurement_interval = 140

    # Instantiate LCDProc
    lcd = Server(debug=False, hostname=lcd_proc_server)
    lcd.start_session()

    # Add screen for air, temperature and humidity
    screenAir = lcd.add_screen("Air")
    #screenAir.set_heartbeat("off")
    screenAir.set_duration(10)

    pm25 = ""
    pm25_value="PM25: " + pm25
    pm25_widget = screenAir.add_string_widget("PM25", x=1, y=1, text=pm25_value)
    pm10 = ""
    pm10_value="PM10: " + pm10
    pm10_widget = screenAir.add_string_widget("PM10", x=1, y=2, text=pm10_value)
    temp = ""
    temp_value="Temp: " + temp
    temp_widget = screenAir.add_string_widget("Temp", x=1, y=3, text=temp_value)
    hu = ""
    humi_value="Humi: " + hu
    humi_widget = screenAir.add_string_widget("Humi", x=1, y=4, text=humi_value)
    update = ""
    update_value="Up: " + update
    update_widget = screenAir.add_string_widget("Up:", x=12, y=4, text=update_value)

    try:
        while True:
            # Poll sensor data
            # page = requests.get('https://raw.githubusercontent.com/herrnikolov/air/master/air.html')
            page = requests.get(air_station)
            tree = html.fromstring(page.content)

            pm25 = tree.xpath('/html/body/div[2]/table/tr[3]/td[3]/text()')
            pm25 = ''.join(pm25)[:4].encode('ascii', 'ignore')
            pm25_value="PM25: " + pm25
            pm25_widget.set_text(pm25_value)
            
            pm10 = tree.xpath('/html/body/div[2]/table/tr[4]/td[3]/text()')
            pm10 = ''.join(pm10)[:4].encode('ascii', 'ignore')
            pm10_value="PM10: " + pm10
            pm10_widget.set_text(pm10_value)

            temp = tree.xpath('/html/body/div[2]/table/tr[6]/td[3]/text()')
            temp = ''.join(temp)[:4].encode('ascii', 'ignore')
            temp_value="Temp: " + temp
            temp_widget.set_text(temp_value)

            hu = tree.xpath('/html/body/div[2]/table/tr[8]/td[3]/text()')
            hu = ''.join(hu)[:4].encode('ascii', 'ignore')
            humi_value="Humi: " + hu
            humi_widget.set_text(humi_value)

            update = tree.xpath('/html/body/div[2]/b/text()')
            update = ''.join(update)[:3].encode('ascii', 'ignore')
            update_value="Up: " + update
            update_widget.set_text(update_value)
            #Wait for update
            sleep(measurement_interval)
        
    finally:     # clean up on exit
        lcd.del_screen(screenAir.ref)
# Run
if __name__ == "__main__":
    main()

#ref: https://www.rototron.info/lcdproc-tutorial-for-raspberry-pi/
#ref: https://github.com/jinglemansweep/lcdproc/blob/master/lcdproc/screen.py
#ref: https://docs.python-guide.org/scenarios/scrape/
#ref: https://programtalk.com/vs2/python/6001/misc-scripts/simpleLCDproc.py/
