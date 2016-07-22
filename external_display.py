import radio
from microbit import display, button_a, sleep, button_b, Image


BASE_CHANNEL = 70
SCREEN_SIZE = 5
MAX_DISPLAY_IDX = 9


def button_incdec():
    get_state = lambda: int(button_b.is_pressed()) - int(button_a.is_pressed())
    initial_state = get_state()
    if initial_state:
        while get_state():
            pass
    return initial_state



def transmit(img):
    """The `microbit.display.show` function on steroids
   
    Image of size 10 x 10 will be divided into following fragments:

    +-------+-------+
    |       |       |
    |   0   |   1   |
    |       |       |
    +-------+-------+
    |       |       |
    |   2   |   3   |
    |       |       |
    +-------+-------+

    0 - local screen (also sent on BASE_CHANNEL + 0 for mirroring capability)
    1 - screen on the BASE_CHANNEL + 1
    2 - screen on the BASE_CHANNEL + 2
    ...
    n - screen on the BASE_CHANNEL + n
    """
    assert img.width() == img.height()
    assert img.height() % SCREEN_SIZE == 0

    fragment_count = img.width() // SCREEN_SIZE

    for y in range(fragment_count):
        for x in range(fragment_count):
            # Extract a fragment from the original image
            frag = img.crop(
		x * SCREEN_SIZE, 
		y * SCREEN_SIZE, 
		SCREEN_SIZE, 
		SCREEN_SIZE
	    )

            # switch the radio channel
            channel = BASE_CHANNEL + (y * fragment_count) + x
            radio.config(channel=channel, length=251)

            # Display the image locally if fragment == 0
            if x == 0 and y == 0:
                display.show(img)


def receive():
    """Starts a receiver program"""
    radio.on()
    channel_idx = 0

    while True:
        # Handle the display switching
        # A for prev channel, B for next channel
        channel_selector = button_incdec()
        if channel_selector != 0:
            # Switch the channel
            channel_idx = (channel_idx + channel_selector) % MAX_DISPLAY_IDX
            radio.config(channel=BASE_CHANNEL + channel_idx, length=251)
            radio.on()
 
            # Give the user some feedback
            display.show(str(channel_idx))
            sleep(1000)
            display.clear()
            
        msg = radio.receive()
        if msg:
            # TODO: validate that we have received a valid frame
            try:
                display.show(eval(msg))
            except Exception as e:
                print(repr(e))


receive()
