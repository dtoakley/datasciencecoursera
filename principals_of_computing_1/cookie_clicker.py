"""
Cookie Clicker Simulator
"""

#import simpleplot

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)
import math
import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._cps = 1.0

        self._history =[(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return "total cookies: {:.2f} \ncurrent cookies: {:.2f} \ncurrent time: {:.2f} \ncps: {:.2f}".format(
        self._total_cookies, self._current_cookies, self._current_time, self._cps)

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        time_until = math.ceil((cookies - self._current_cookies) / self._cps)
        if time_until < 0:
            return 0.0
        else:
            return time_until

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._current_time += time
            self._current_cookies += time * self._cps
            self._total_cookies += time * self._cps

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies))

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_info = build_info.clone()
    clicker_state = ClickerState()

    while clicker_state.get_time() <= duration:
        time_left = duration - clicker_state.get_time()

        item_name = strategy(clicker_state.get_cookies(), clicker_state.get_cps(),
                    clicker_state.get_history(), time_left, build_info)
        if item_name is None:
            break
        item_cost = build_info.get_cost(item_name)
        time_to_purchase = clicker_state.time_until(item_cost)

        if time_to_purchase > time_left:
            break

        clicker_state.wait(time_to_purchase)
        clicker_state.buy_item(item_name, item_cost, build_info.get_cps(item_name))
        build_info.update_item(item_name)

    clicker_state.wait(time_left)
    return clicker_state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = build_info.build_items()
    cookies_possible = cookies + cps * time_left
    cheapest_item = None
    cost_of_chepeast_item = float("inf")

    for item in items:
        item_cost = build_info.get_cost(item)
        if item_cost <= cookies_possible and item_cost < cost_of_chepeast_item:
            cost_of_chepeast_item = item_cost
            cheapest_item = item

    return cheapest_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    cookies_possible = cookies + cps * time_left
    expensive_item = None
    cost_of_expensive_item = 0

    for item in items:
        item_cost = build_info.get_cost(item)
        if item_cost <= cookies_possible and item_cost > cost_of_expensive_item:
            cost_of_expensive_item = item_cost
            expensive_item = item

    return expensive_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    items = build_info.build_items()
    cookies_possible = cookies + cps * time_left
    best_roi = 0
    best_item = None

    for item in items:
        item_cost = build_info.get_cost(item)
        item_roi = build_info.get_cps(item) / item_cost
        if item_roi > best_roi and item_cost <= cookies_possible:
            best_roi = item_roi
            best_item = item

    return best_item

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

run()
