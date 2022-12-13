def on_button_pressed_a():
    enviaDatos()

input.on_button_pressed(Button.A, on_button_pressed_a)

def on_mqtt_qos_list_qos0(message):
    if message == "On":
        smarthome.relay(DigitalPin.P16, smarthome.RelayStateList.OFF)
        OLED.write_string_new_line("Rele On")
    else:
        smarthome.relay(DigitalPin.P16, smarthome.RelayStateList.ON)
        OLED.write_string_new_line("Rele Off")

ESP8266_IoT.mqtt_event("IOTbit01/rele",
    ESP8266_IoT.QosList.QOS0,
    on_mqtt_qos_list_qos0)

def enviaDatos():
    global envios
    if ESP8266_IoT.is_mqtt_broker_connected():
        ESP8266_IoT.publish_mqtt_message(convert_to_text(smarthome.read_temperature(TMP36Type.TMP36_TEMPERATURE_C, AnalogPin.P2)),
            "" + nombre + "/Temp",
            ESP8266_IoT.QosList.QOS0)
        ESP8266_IoT.publish_mqtt_message(convert_to_text(Environment.read_light_intensity(AnalogPin.P1)),
            "" + nombre + "/Luz",
            ESP8266_IoT.QosList.QOS0)
        envios += 1
        ESP8266_IoT.publish_mqtt_message(convert_to_text(envios),
            "" + nombre + "/envios",
            ESP8266_IoT.QosList.QOS0)
        OLED.write_string_new_line("T:" + convert_to_text(smarthome.read_temperature(TMP36Type.TMP36_TEMPERATURE_C, AnalogPin.P2)) + " l:" + str(Environment.read_light_intensity(AnalogPin.P1)) + " e:" + convert_to_text(envios))
        basic.show_icon(IconNames.HEART)
    else:
        basic.show_icon(IconNames.SKULL)
        OLED.write_string_new_line("Error MQTT")
        
envios = 0
nombre = ""
nombre = "IOTbit01"
OLED.init(128, 64)
basic.show_number(0)
OLED.write_string_new_line("IOT:bit 0.4")
ESP8266_IoT.init_wifi(SerialPin.P8, SerialPin.P12, BaudRate.BAUD_RATE115200)
basic.show_number(1)
ESP8266_IoT.connect_wifi("OpenWrt", "qazxcvbgtrewsdf")
OLED.write_string_new_line("Wifi ok")
basic.show_number(2)
ESP8266_IoT.set_mqtt(ESP8266_IoT.SchemeList.TCP, nombre, "", "", "")
basic.show_number(3)
ESP8266_IoT.connect_mqtt("192.168.1.100", 1883, True)
basic.show_number(4)

def on_every_interval():
    enviaDatos()
loops.every_interval(60000, on_every_interval)
