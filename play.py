from Connection import Connection
from Config import Config
import time
from Supply import Supply
import random

config = Config('config.json')
connection = Connection(config=config)
supplies = Supply(config=config)

planets = config.planets()

min_delay_minutes = 1
max_delay_minutes = 5

# Login or relogin to ensure the connection is not timed out
empire = connection.connect()
print("Planet list")
print(empire.planet_ids())

@empire.keep_going
def run():
    while True:

        for planet_id in planets:
            # Just to help in the script debugging
            planet_name = empire.name_by_planet_id(planet_id)
            print("Planet " + str(planet_name))

            actual_resources = empire.resources(planet_id)

            print("resources (metal, crystal, deuterium)")
            print(actual_resources.resources)

            # Do things
            action = supplies.next(empire, planet_id)

            if action is not None:
                print("Building...")
                empire.build(what=action, id=planet_id)

            print("\n", flush=True)

            time.sleep(60) #if not the session is closed (banned?)

        # Wait
        delay = random.randrange(min_delay_minutes, max_delay_minutes)*60
        print("Waiting for " + str(int(delay/60)) + " minutes")
        print("---------------------------\n", flush=True)

        time.sleep(delay)

if __name__ == "__main__":
    run()