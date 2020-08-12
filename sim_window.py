import datetime
import constants
import easygui as eg  # https://github.com/robertlugg/easygui   - easy way to open file dialog and other gui things.

from Map import *


FPS = 30
ACTIVE_BUTT_COLOR = pygame.Color('dodgerblue1')
INACTIVE_BUTT_COLOR = pygame.Color('dodgerblue4')
pygame.font.init()
FONT = pygame.font.Font(None, 30)


# TODO: limit movement (drone get stuck in walls)
# displaying the screen.
def display_all(main_surface, display_list, text_list):
    for element in display_list:
        element.display(main_surface)
    for element_val in range(0, len(text_list)):  # adding text in the side of the screen
        main_surface.blit(font.render(str(text_list[element_val]), True, (0, 255, 0)), (10, 10 + (20 * element_val)))


# update all elements in list.
def update_all(update_list):
    for element in update_list:
        element.update()


# drawing the button on pygame canvas.
def draw_button(button, screen):
    """Draw the button rect and the text surface."""
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


# creating a simple button in pygame
def create_button(x, y, w, h, text):
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    text_surf = FONT.render(text, True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_BUTT_COLOR,
    }
    return button


clock = pygame.time.Clock()
font = pygame.font.SysFont("", 20)
pygame.init()  # initialize pygame window
print("###########~~INIT SIMULATOR WINDOW~~###########")


# TODO: Enable for map selection dialog and remove constant 
# map_image_path = eg.fileopenbox()  # opens a file choosing dialog.
map_image_path = constants.MAP_IMAGE_PATH

game_map = Map(map_image_path)  # setting map object, map choosing is inside the object.

game_map.create_map_from_img()
main_s = pygame.display.set_mode((game_map.map_width, game_map.map_height))  # our main display
drone = SimpleDrone(100, 300, main_s, game_map)  # drone object, starting from coordinates 100,300
sim_map = pygame.image.load(constants.TMP_MAP_PATH).convert()  # loading the map with the temp name given.

# button creation
auto_manual_button = create_button(game_map.map_width - 180, game_map.map_height - 50, 180, 50, 'Manual/Auto')
track_button = create_button(game_map.map_width - 180, game_map.map_height - (100 + 1), 180, 50, 'Track')
pause_button = create_button(game_map.map_width - 180, game_map.map_height - (150 + 2), 180, 50, 'Quit')
log_button = create_button(game_map.map_width - 180, game_map.map_height - (200 + 3), 180, 50, 'Toggle CsvLogging')
# button in the right-down corner.
button_list = [auto_manual_button, track_button, pause_button, log_button]  # a list containing all buttons

pygame.time.set_timer(pygame.USEREVENT, 1000)
time = datetime.datetime.min
running = True  # simulation is running
logging = False
log_file = ""  # if logging is needed.

while running:
    clock.tick(FPS)
    time += datetime.timedelta(0, (FPS / 10))

    main_s.fill(BLACK)  # resets the map every loop.
    main_s.blit(sim_map, (0, 0))  # filling screen with map
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                for button in button_list:
                    # `event.pos` is the mouse position.
                    if button['rect'].collidepoint(event.pos):
                        # execute function in the state machine
                        # drone.state = drone.state.on_event('switch_state')
                        if button == button_list[0]:  # manual/auto button
                            if drone.event == 'manual_control':  # switch states
                                drone.event = 'auto_control'
                                drone.on_event('auto_control')
                            else:
                                drone.event = 'manual_control'
                                drone.on_event('manual_control')
                        if button == button_list[1]:  # tracking on/off button
                            if drone.tracking:
                                drone.tracking = False
                            else:
                                drone.tracking = True
                        if button == button_list[2]:  # quit button
                            if running:
                                csv_f = open('csvfile.csv', 'w')  # handling logging to csv file before closing.
                                csv_f.write(log_file)
                                csv_f.close()
                                running = False
                        if button == button_list[3]:
                            if not logging:
                                logging = True
        elif event.type == pygame.MOUSEMOTION:
            # When the mouse gets moved, change the color of the
            # buttons if they collide with the mouse.
            for button in button_list:
                if button['rect'].collidepoint(event.pos):
                    button['color'] = ACTIVE_BUTT_COLOR
                else:
                    button['color'] = INACTIVE_BUTT_COLOR
    if drone.event == 'manual_control':  # if we are in manual control
        drone.on_event('manual_control')
    # TODO: a method for logging key pressings.
    # TODO: implement autostate
    # need to implement auto state

    to_update = [drone]  # update drone variables
    to_display = [drone]  # update drone displaying on map.

    to_text = ["FPS: " + str("%.0f" % clock.get_fps()),  # our telemetry window.
               "Drone angle: " + str("%.2f" % drone.angle),
               "Current speed: " + str("%.2f" % drone.current_speed),
               "X Axis Movement: " + str("%.2f" % drone.move_x),
               "Y Axis movement: " + str("%.2f" % drone.move_y),
               "F key" + str(drone.forward),
               "L key" + str(drone.left),
               "R key" + str(drone.right),
               "B key" + str(drone.backward),
               "Collided: " + str(drone.is_colliding),
               "Collision Detected: " + str(drone.front_detect),
               "Time: " + str('{0:%H:%M:%S}'.format(time))]

    to_log = [str("%.0f" % clock.get_fps()),  # our telemetry window.
              str("%.2f" % drone.angle), str("%.2f" % drone.current_speed), str("%.2f" % drone.move_x),
              str("%.2f" % drone.move_y), str(drone.forward), str(drone.left), str(drone.right), str(drone.backward),
              str(drone.is_colliding), str(drone.front_detect), str('{0:%H:%M:%S}'.format(time))]

    # HANDLING CSV LOGGING
    if logging:
        line = ""
        for text in to_text:
            line += text + ","
        line = line[:-1]
        line += "\n"
        log_file += line

    for button in button_list:
        draw_button(button, main_s)
    update_all(to_update)
    display_all(main_s, to_display, to_text)
    pygame.display.flip()  # show the surface we created on the actual screen.
