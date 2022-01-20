from level.LevelCreator import LevelCreator


# def main():
#
#     display_manager = DisplayManager()
#     display_manager.create_window(1280, 720, "Level Creator")
#
#     projection_matrix = pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)
#
#     # Test OpenGL
#
#     rects = []
#
#     def window_to_projection(pos, proj):
#         pos = np.array(pos, dtype=np.float32)
#         proj = np.array(proj, dtype=np.float32)
#         dims = np.array([display_manager.width, display_manager.height], dtype=np.float32)
#         pos = pos / dims  # 0 to 1
#         pos = pos * 2 - 1  # -1 to 1
#         pos[1] *= -1  # Since y goes up not down
#         pos = pos * proj
#         return pos
#
#
#     def on_mouse_left():
#         cursor_pos = window_to_projection(display_manager.get_cursor_pos(), [16, 9])
#         cursor_pos.resize((1, 3))
#         cursor_tile = np.floor(cursor_pos + camera.position).astype(np.int32)
#         if level.collision_chunks[cursor_tile[0]][cursor_tile[1]]:
#             level.collision_chunks[cursor_tile[0]][cursor_tile[1]] = False
#             # Find rect
#             rects.pop(find_rect((cursor_tile[0], cursor_tile[1])))
#
#         else:
#             level.collision_chunks[cursor_tile[0]][cursor_tile[1]] = True
#             rects.append(Rect(cursor_tile, (1, 1), np.append(np.random.random(3), 1)))
#
#     display_manager.bind_mouse_left(on_mouse_left)
#
#
#     def find_rect(pos):
#         for count, rect in enumerate(rects):
#             if rect.position == pos:
#                 return count
#
#     def gen_tiles():
#         for i in range(len(level.collision_chunks)):
#             for j in range(len(level.collision_chunks[i])):
#                 if level.collision_chunks[i][j]:
#                     rects.append(Rect((i, j), (1, 1), np.append(np.random.random(3), 1)))
#
#     level = Level()
#     level.collision_chunks = np.random.random_sample((32, 32)) > 0.5
#     gen_tiles()
#
#     cursor_rect = Rect((0, 0), (1, 1), (1, 0, 0, 0.5))
#     rects.append(cursor_rect)
#
#     main_renderer = MainRenderer(projection_matrix)
#     camera = Camera()
#
#     glClearColor(1.0, 1.0, 1.0, 1.0)
#     while not display_manager.window_should_close():
#         display_manager.start_frame()
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         glDepthFunc(GL_LEQUAL)
#         glEnable(GL_DEPTH_TEST)
#         cursor_pos = window_to_projection(display_manager.get_cursor_pos(), [16, 9])
#         cursor_pos.resize((1, 3))
#         cursor_rect.position = np.floor(cursor_pos + camera.position)
#
#         if display_manager.get_key_state(glfw.KEY_A):
#             camera.position[0] -= 0.1
#         elif display_manager.get_key_state(glfw.KEY_D):
#             camera.position[0] += 0.1
#         elif display_manager.get_key_state(glfw.KEY_W):
#             camera.position[1] += 0.1
#         elif display_manager.get_key_state(glfw.KEY_S):
#             camera.position[1] -= 0.1
#
#
#         main_renderer.render([], [], rects, [], camera)
#
#         display_manager.update_display()

def main():
    level_creator = LevelCreator()
    level_creator.run()


if __name__ == '__main__':
    main()