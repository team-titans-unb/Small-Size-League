from calendar import c
from itertools import count
import time
from constants import TEAM_COLOR, LOOP_SLEEP_S
from system_logic import initialize_system, process_robot_logic, stop_all_robots
from utils.logger import setup_logger

def main():
    """
    The main entry point of the program.
    Orchestrates the system initialization and the main processing loop.
    """
    logger = setup_logger('main', 'logs/main.log')
    logger.info("Starting the Robot Control System...")
    components = initialize_system()
    if not components:
        logger.error("Failed to initialize system components.")
        return

    try:
        vision_client = components['vision_client']
        vision_parser = components['vision_parser']
        gc_client = components['gc_client']
        gc_parser = components['gc_parser']

        while True:
            # 1. Get the latest data from the vision system
            vision_raw_data = vision_client.get_last_data()
            if vision_raw_data is not None:
                vision_parser.parser_loop(vision_raw_data)
                # print ("--------- DADOS DO VISION PARSER ---------\n")
                # print (vision_parser.get_last_detection())
                # print ("\n------------------------------------------\n")

            ## ---------------------
            ## GET GC DATA (do nothing for now)
            gc_raw_data = gc_client.get_last_data()
            if gc_raw_data is not None:
                gc_parser.parser_loop(gc_raw_data)
                # print ("--------- DADOS DO GC PARSER ---------\n")
                # print (gc_parser.get_last_data())
                # print ("\n------------------------------------------\n")

            # 2. If we have data, process it
            if vision_parser and vision_parser.get_last_detection():
                #print ("Vision data received.")
                detection = vision_parser.get_last_detection()
                our_robots = detection['robots'].get(TEAM_COLOR, [])
                #print (our_robots)
                ball_info = detection['balls'][0] if detection.get('balls') else None
                #print (ball_info)

                for robot_info in our_robots:
                    # 3. Process each robot's logic
                    print (f"Processing logic to robot ID {robot_info['robot_id']}...")
                    process_robot_logic(robot_info, ball_info, components)
            else:
                # If no data, tell all robots to stop
                #print ("No vision data received. Stopping all robots.")
                stop_all_robots(components['robot_senders'])

            time.sleep(0.01)

    except KeyboardInterrupt:
        logger.info("Program interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if components:
            logger.info("Shutting down the system...")
            logger.info("Stopping all robots...")
            stop_all_robots(components['robot_senders'])
            if components.get('vision_client'):
                components['vision_client'].stop()
                logger.info("Disconnected from Vision...")

if __name__ == '__main__':
    main()