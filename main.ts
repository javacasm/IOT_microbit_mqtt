input.onButtonPressed(Button.A, function () {
    enviaDatos()
})
ESP8266_IoT.MqttEvent("IOTbit01/rele", ESP8266_IoT.QosList.Qos0, function (message) {
    if (message == "On") {
        smarthome.Relay(DigitalPin.P16, smarthome.RelayStateList.Off)
        OLED.writeStringNewLine("Rele On")
    } else {
        smarthome.Relay(DigitalPin.P16, smarthome.RelayStateList.On)
        OLED.writeStringNewLine("Rele Off")
    }
})
function enviaDatos () {
    if (ESP8266_IoT.isMqttBrokerConnected()) {
        ESP8266_IoT.publishMqttMessage(convertToText(smarthome.ReadTemperature(TMP36Type.TMP36_temperature_C, AnalogPin.P2)), "" + nombre + "/Temp", ESP8266_IoT.QosList.Qos0)
        ESP8266_IoT.publishMqttMessage(convertToText(Environment.ReadLightIntensity(AnalogPin.P1)), "" + nombre + "/Luz", ESP8266_IoT.QosList.Qos0)
        envios += 1
        ESP8266_IoT.publishMqttMessage(convertToText(envios), "" + nombre + "/envios", ESP8266_IoT.QosList.Qos0)
        OLED.writeStringNewLine("T:" + convertToText(smarthome.ReadTemperature(TMP36Type.TMP36_temperature_C, AnalogPin.P2)) + " l:" + ("" + Environment.ReadLightIntensity(AnalogPin.P1)) + " e:" + convertToText(envios))
        basic.showIcon(IconNames.Heart)
    } else {
        basic.showIcon(IconNames.Skull)
        OLED.writeStringNewLine("Error MQTT")
    }
}
let envios = 0
let nombre = ""
nombre = "IOTbit01"
OLED.init(128, 64)
basic.showNumber(0)
OLED.writeStringNewLine("IOT:bit 0.4")
ESP8266_IoT.initWIFI(SerialPin.P8, SerialPin.P12, BaudRate.BaudRate115200)
basic.showNumber(1)
ESP8266_IoT.connectWifi("OpenWrt", "qazxcvbgtrewsdf")
OLED.writeStringNewLine("Wifi ok")
basic.showNumber(2)
ESP8266_IoT.setMQTT(
ESP8266_IoT.SchemeList.TCP,
nombre,
"",
"",
""
)
basic.showNumber(3)
ESP8266_IoT.connectMQTT("192.168.1.100", 1883, true)
basic.showNumber(4)
loops.everyInterval(60000, function () {
    enviaDatos()
})
