import paho.mqtt.client as mqtt
import asyncio
import kasa
import json

MQTT_HOST = "tbox"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected: {reason_code}")
    client.subscribe("home/events")

async def turn(dev_num, next_state):
    dev = await kasa.Discover.discover_single(f'192.168.1.{dev_num}')
    if next_state: await dev.turn_on()
    else: await dev.turn_off()
    await dev.update()

def on_message(client, userdata, msg):
    print(f' {msg.topic:^27} {msg.payload}')
    pl = json.loads(msg.payload.decode('utf8'))
    try:
        asyncio.run(turn(pl["id"], pl["state"]))
    except kasa.exceptions.TimeoutError:
        print("Timed out!")

def main():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(MQTT_HOST, 1883, 60)

    mqttc.loop_forever()


if __name__ == "__main__":
    main()
