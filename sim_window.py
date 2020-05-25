from Drone import *

drone = SimpleDrone(200, 300)
pygame.font.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont("", 20)

pygame.init()
game_map = Map("future path here")
main_s = pygame.display.set_mode((game_map.map_width, game_map.map_height))
sim_map = pygame.image.load('new_map.png')


def display_all(main_surface, display_list, text_list):
    # main_surface.fill((0, 100, 100))

    for element in display_list:
        element.display(main_surface)
    for element_val in range(0, len(text_list)):  # adding text in the side of the screen
        main_surface.blit(font.render(str(text_list[element_val]), True, (0, 255, 0)), (10, 10 + (20 * element_val)))


def update_all(update_list):
    for element in update_list:
        element.update()


running = True
while running:
    clock.tick(60)
    main_s.fill((0, 0, 0))
    main_s.blit(sim_map, (0, 0))  # filling screen with map
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # TODO: a mathod for logging key pressings.
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        drone.left = True
    if key[pygame.K_RIGHT]:
        drone.right = True
    if key[pygame.K_UP]:
        drone.forward = True
    if key[pygame.K_DOWN]:
        drone.backward = True
    if key[pygame.K_r]:
        drone.start_loc_x = 500
        drone.start_loc_y = 300
        drone.angle = 0

    to_update = [drone]
    to_display = [drone]
    to_text = ["FPS: " + str("%.0f" % clock.get_fps()),
               "Drone angle: " + str("%.2f" % drone.angle),
               "Current speed: " + str("%.2f" % drone.current_speed),
               "X Axis Movement: " + str("%.2f" % drone.move_x),
               "Y Axis movement: " + str("%.2f" % drone.move_y),
               "F key" + str(drone.forward),
               "L key" + str(drone.left),
               "R key" + str(drone.right)]

    update_all(to_update)
    display_all(main_s, to_display, to_text)
    pygame.display.flip()
