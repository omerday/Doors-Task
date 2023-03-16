import random
import datetime
import pandas
from psychopy import core, visual, event
import time
import pygame

DOOR_IMAGE_PATH_PREFIX = './img/doors1/'
OUTCOMES_IMAGE_PREFIX = './img/outcomes/'
IMAGE_SUFFIX = '.jpg'


def setup_door(window, params, punishment: int, reward: int):
    """
    Show door corresponding to the reward and punishment sent as arguments. Chooses the size in which it starts
    either randomly or fixed according to the parameters in order to be able to zoom out nicely.
    :param params: parameters from the main run
    :param window: psychopy windows object
    :param reward: reward (1-7)
    :param punishment: punishment (1-7)
    :return: image: the image object that will be used for movements
    :return: location: the relative location of the subject from the door, should be 1-100
    """
    isRandom = params['startingDistance'] == 'Random'
    location = round(0.6 - 0.1 * random.random(), 2) if isRandom else params[
                                                                'startingDistance'] / 100  # a variable for the relative location
    # of the subject from the door, should be 0-1
    imagePath = DOOR_IMAGE_PATH_PREFIX + f"p{punishment}r{reward}" + IMAGE_SUFFIX

    image = visual.ImageStim(window, image=imagePath,
                             size=((1.5 + location), (1.5 + location)),
                             units="norm", opacity=1)

    image.draw()
    window.update()
    return image, location


def move_screen(window, params, image: visual.ImageStim, location, units):
    """
    The method brings the image closer or further from the subject, according to the units of movement given.
    The units are converted from 1-100 to 0-1, and added to the location.
    :param window:
    :param params:
    :param image:
    :param location:
    :param units:
    :return: image: the updated image object
    :return: location: the updated location. Will be used to determine the chance of the door opening.
    """
    location = location + units / 100
    image.size = (1.5 + location, 1.5 + location)
    image.draw()
    window.update()
    return image, location


def get_movement_input_keyboard(window, params, image: visual.ImageStim, location, end_time: time.time,
                                Df: pandas.DataFrame, dict: dict):
    """
    The method gets up/down key state and moves the screen accordingly.
    The method requires pygame to be installed (and therefore imported to Psychopy if needed).
    :param dict:
    :param Df:
    :param window:
    :param params:
    :param image:
    :param location:
    :param end_time:
    :return: location, Df and dictionary
    """

    pygame.init()
    while time.time() < end_time:
        pygame.event.clear()
        # pygame.event.pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                core.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_SPACE]:
            if location < 0.97:
                image, location = move_screen(window, params, image, location, params['sensitivity'] * 0.5)
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_SPACE]:
            if location > 0.1:
                image, location = move_screen(window, params, image, location, params['sensitivity'] * (-0.5))
        elif keys[pygame.K_ESCAPE]:
            core.quit()
        elif keys[pygame.K_SPACE] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            spacePress = True
            while spacePress:
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                        spacePress = False
                        break
            break

        # Update dict
        dict['CurrentTime'] = round(time.time() - dict['StartTime'], 3)
        dict['CurrentDistance'] = round(location, 2)
        if location > dict['MaxDistance']:
            dict['MaxDistance'] = round(location, 2)
        if location < dict['MinDistance']:
            dict['MinDistance'] = round(location, 2)

        # Update Df:
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
    return location, Df, dict


def get_movement_input_joystick(window, params, image: visual.ImageStim, location, end_time: time.time):
    pass


def start_door(window: visual.Window, params, image: visual.ImageStim, punishment: int, reward: int, location,
               Df: pandas.DataFrame, dict: dict):
    # Set end time for 10s max
    start_time = time.time()
    end_time = start_time + 10

    # Add initial dict parameters
    dict['RoundStartTime'] = round(time.time() - dict['StartTime'], 3)
    dict['CurrentDistance'] = location, 2
    dict['MaxDistance'] = location
    dict['MinDistance'] = location

    if params['keyboardMode']:
        location, Df, dict = get_movement_input_keyboard(window, params, image, location, end_time, Df, dict)
    else:
        # TODO: take joystick into consideration.
        pass

    total_time = time.time() - start_time
    dict["LockTime"] = total_time
    dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])

    # Seed randomization for waiting time and for door opening chance:
    random.seed(time.time() % 60)  # Seeding using the current second in order to have relatively random seed
    doorWaitTime = 2 + random.random() * 2 # Randomize waiting time between 2-4 seconds
    waitStart = time.time()

    dict["DoorWaitTime"] = doorWaitTime
    while time.time() < waitStart + doorWaitTime:
        dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
        Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
        core.wait(1/1000)

    # Randomize door opening chance according to location:
    doorOpenChance = random.random()
    isDoorOpening = doorOpenChance <= location

    dict["DidDoorOpen"] = 1 if isDoorOpening else 0
    dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
    Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])

    if isDoorOpening:
        # Randomize the chances for p/r. If above 0.5 - reward. else - punishment.
        rewardChance = random.random()
        if rewardChance >= 0.5:
            image.setImage(OUTCOMES_IMAGE_PREFIX + f'{reward}_reward' + IMAGE_SUFFIX)
            image.setSize((2, 2))
            image.draw()
            window.update()
            coins = reward
            dict["DidWin"] = 1
        else:
            image.setImage(OUTCOMES_IMAGE_PREFIX + f'{punishment}_punishment' + IMAGE_SUFFIX)
            image.setSize((2, 2))
            image.draw()
            window.update()
            coins = -1 * punishment
            dict["DidWin"] = 0

        waitTimeStart = time.time()
        while time.time() < waitTimeStart + 2:
            dict["CurrentTime"] = round(time.time() - dict['StartTime'], 3)
            Df = pandas.concat([Df, pandas.DataFrame.from_records([dict])])
            core.wait(1/1000)

        return coins, total_time, Df, dict

    else:
        return 0, total_time, Df, dict
