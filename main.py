import microbit
from microbit import display, Image, button_a

# The event loop
def event_loop(tasks):
    run_queue = [t() for t in tasks if t is not None]
    while run_queue:
        t = run_queue.pop(0)
        try:
            next(t)
            run_queue.append(t)
        except StopIteration:
            pass


# Wrappers for the standard library
def sleep(msecs):
    t = microbit.running_time()
    while microbit.running_time() < t + msecs:
        yield


def wait_for_button_press(button):
    while not button.is_pressed():
        yield


def scroll(string, delay=150, loop=False, monospace=False):
    display.scroll(string, delay, wait=False,
                   loop=loop, monospace=monospace)
    yield from sleep(delay * 5 * (len(string) + 1))

    
# Initializing Skynet
def task_1():
    display.show(Image.CLOCK1)
    yield from sleep(2000)
    display.show(Image.CLOCK3)
    yield from sleep(2000)
    display.show(Image.CLOCK5)


def task_2():
    yield from sleep(1000)
    display.show(Image.CLOCK2)
    yield from sleep(2000)
    display.show(Image.CLOCK4)
    yield from sleep(2000)
    display.show(Image.CLOCK6)


def task_3():
    yield from wait_for_button_press(button_a)
    yield from scroll('The end')
    display.scroll('---')


tasks = [
    task_1,
    task_2,
    task_3
]

event_loop(tasks)
