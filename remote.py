import paho.mqtt.client as mqtt
import asyncio
from kasa import Discover
import json

MQTT_HOST = "tbox"
IP_NUMS={"two":"192.168.1.138",
	"one":"192.168.1.199",
	"four":"192.168.1.101"}

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected: {reason_code}")
    client.subscribe("DroidPad/Events")

async def turn(dev_num, next_state):
    dev = await Discover.discover_single(IP_NUMS[dev_num])
    if next_state: await dev.turn_on()
    else: await dev.turn_off()
    await dev.update()

def on_message(client, userdata, msg):
    print(f' {msg.topic:^27} {msg.payload}')
    pl = json.loads(msg.payload.decode('utf8'))
    asyncio.run(turn(pl["id"], pl["state"]))

def main():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(MQTT_HOST, 1883, 60)

    mqttc.loop_forever()


if __name__ == "__main__":
    main()
