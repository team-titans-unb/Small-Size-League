import time
from constants import TEAM_COLOR, LOOP_SLEEP_S
from system_logic import initialize_system, process_robot_logic, stop_all_robots

def main():
    """
    The main entry point of the program.
    Orchestrates the system initialization and the main processing loop.
    """
    print ("Starting the Robot Control System...")
    components = initialize_system()
    if not components:
        print ("Failed to initialize system components.")
        return # Exit if initialization failed

    try:
        while True:
            # 1. Get the latest data from the vision system
            vision_data = components['vision_receiver'].receive_data()

            # 2. If we have data, process it
            if vision_data and vision_data.get('detection'):
                print ("Vision data received.")
                detection = vision_data['detection']
                our_robots = detection['robots'].get(TEAM_COLOR, [])
                ball_info = detection['balls'][0] if detection.get('balls') else None

                for robot_info in our_robots:
                    # 3. Process each robot's logic
                    print (f"Processing logic to robot ID {robot_info['robot_id']}...")
                    process_robot_logic(robot_info, ball_info, components)
            else:
                # If no data, tell all robots to stop
                print ("No vision data received. Stopping all robots.")
                stop_all_robots(components['robot_senders'])

            time.sleep(LOOP_SLEEP_S)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if components:
            print ("Shutting down the system...")
            print ("Stopping all robots...")
            stop_all_robots(components['robot_senders'])
            if components.get('vision_client'):
                components['vision_client'].disconnect()
                print("Disconnected from Vision...")

if __name__ == '__main__':
    main()