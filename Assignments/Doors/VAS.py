import helpers
from psychopy import visual, core
from psychopy.visual import ratingscale

QUESTIONS_BEGINNING_MIDDLE = ["How anxious do you feel right now?",
                              "How much do you feel like taking part in the task?",
                              "How tired are you right now?",
                              "Think about your mood right now. How would you describe it?"]
ANSWERS_BEGINNING_MIDDLE = [["Not anxious", "Very anxious"], ["Not at all", "Very much"],
                            ["Not tired at all", "Very tired"],
                            ["Worst mood possible", "Best mood possible"]]
QUESTIONS_FINAL = ["How many coins do you think you won?", "How many coins do you think you lost?", "How often did "
                                                                                                    "you see the "
                                                                                                    "monster when the "
                                                                                                    "door opened?",
                   "How often did you win coins when the door opened?", "How do you feel about how well you’ve done "
                                                                        "so far?"]
ANSWERS_FINAL = [["Won very few", "Won very many"], ["Lost very few", "Lost very many"], ["never", "all the time"],
                 ["never", "all the time"], ["sad, I did badly", "happy, I did great"]]


def beginning_vas(window: visual.Window, params):
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE)):
        answer, time = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE[i], ANSWERS_BEGINNING_MIDDLE[i])
        # TODO: Add to DF


def middle_vas(window: visual.Window, params, coins: int):
    for i in range(len(QUESTIONS_BEGINNING_MIDDLE)):
        answer, time = helpers.display_vas(window, params, QUESTIONS_BEGINNING_MIDDLE[i], ANSWERS_BEGINNING_MIDDLE[i])
    if params["keyboardMode"]:
        message = visual.TextStim(window, text=f"Let’s rest for a bit. You have {coins} coins. Press Space when you "
                                               f"are ready to keep playing.", units="norm", color=(255, 255, 255))
    else:
        message = visual.TextStim(window, text=f"Let’s rest for a bit. You have {coins} coins. Click when you "
                                               f"are ready to keep playing.", units="norm", color=(255, 255, 255))
    message.draw()
    window.update()
    if params["keyboardMode"]:
        helpers.wait_for_space(window)
    else:
        helpers.wait_for_click(window)


def final_vas(window: visual.Window, params):
    for i in range(len(QUESTIONS_FINAL)):
        answer, time = helpers.display_vas(window, params, QUESTIONS_FINAL[i], ANSWERS_FINAL[i])