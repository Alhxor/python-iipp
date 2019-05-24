import simplegui
import math

# define global variables
time = 0
watch = "00:00.0"
wins = 0
tries = 0
clock_x = 250.0
clock_y = 110.0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """
    Converts integer <t> into a formatted string,
    such as mm:ss.d, where:
    mm   minutes
    ss   seconds
    d    deciseconds
    """
    min = t / 600
    dsec = t % 10
    sec = (t % 600 - dsec) / 10
    result = ""
    
    # adding extra zero to seconds if needed
    if sec < 10:
        result = ":0" + str(sec) + "." + str(dsec)
    else:
        result = ":" + str(sec) + "." + str(dsec)
    
    # adding extra zero to minutes if needed
    if min < 10:
        result = "0" + str(min) + result
    else:
        result = str(min) + result    

    return result
    

# define event handlers for buttons; "Start", "Stop", "Reset"
def btn_start_handler():
    if not timer.is_running() and time < 36000:
        timer.start()

def btn_stop_handler():
    global wins, tries
    if timer.is_running():
        timer.stop()
        tries += 1
        if watch[6] == "0":
            wins += 1

def btn_reset_handler():
    global time, watch, wins, tries
    if timer.is_running():
        timer.stop()
    time = 0
    watch = format(time)
    wins = 0
    tries = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time, watch, secret_msg, clock_x, clock_y
    if time >= 35999:
        timer.stop()
        print "This timer was running for a whole hour and is now tired... Come back later."
    time += 1
    watch = format(time)
    clock_x = 40 * math.cos(time/96) + 250
    #print 40*math.cos(time)
    clock_y = 40 * math.sin(time/96) + 150
    #print 40*math.sin(time)
    #print clock_x, clock_y # = 250, 110
    if clock_x >= 289.99:
        timer.stop()
        print time
        print clock_x, clock_y
    #if (time >= 600):
    #    timer.stop()


# define draw handler
def draw_handler(canvas):
    canvas.draw_text(watch, [80, 110], 44, "White", "sans-serif")
    canvas.draw_text(str(wins) + '/' + str(tries),
                     [30, 160], 24, "Red", "monospace")
    canvas.draw_circle([250, 150], 40, 5, "#0000BB")

    canvas.draw_line([250, 150], [clock_x, clock_y], 4, "Red")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)

# register event handlers
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(100, timer_handler)
btn_start = frame.add_button("Start", btn_start_handler, 100)
btn_stop = frame.add_button("Stop", btn_stop_handler, 100)
btn_reset = frame.add_button("Reset", btn_reset_handler, 100)

#clock_x = 40 * math.cos(6*(time/10)) + 250
#print clock_x # = 250
#clock_y = 40 * math.sin(6*(time/10)) + 150
#print clock_y # = 110

# start frame
frame.start()

