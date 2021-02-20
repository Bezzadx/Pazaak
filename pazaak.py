from pazaak_play_game import *
from pazaak_human import *
from pazaak_bot import *
from pazaak_ai import *
from pazaak_performance_test import *
from pazaak_train_AI import *

"""
Usage: importing pazaak.py should import all the required functions, classes and methods
to play pazaak through python interactive mode. To play a game, run play(a,b), where a
and b are instances of the classes human, bot, or AI. These classes can all be instantiated using a = AI(), b = bot(), h = human() etc. or an AI can be instantiated using a = train(n), where n will specify the number of training matches it plays. The default value for n is 50,000, which is also the number of training games the default AI instance has trained on. 
Finally, to observe the relative performance of two
different agents, run performance(agent1, agent2, no. of matches). Note that agent 1 is always first to play, so .
"""

colorama_init()