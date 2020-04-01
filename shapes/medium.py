# from .basic import Rectangle as _Rectangle
# from .text import TextDisplay as _TextDisplay
# from ..output.display import Screen as _Screen
# from ..constants import Align as _Al
#
#
# class ProgressBar(_Rectangle):
#     def __init__(self, x=0, y=0, width=None, height=None, color=None, x_mode=_Al.df(), y_mode=_Al.df(), x_offset=0,
#                  y_offset=0, total_progress=1, horizontal=True):
#         _Rectangle.__init__(self, x, y, width, height, color, x_mode, y_mode, x_offset, y_offset)
#         self.total_progress = total_progress
#         self.progress = 0
#         self.horizontal = horizontal
#
#     def set_progress(self, progress):
#         if self.total_progress == 1:
#             self.progress = progress
#         else:
#             self.progress = progress / self.total_progress
#         self.check_progress()
#
#     def set_percentage(self, percentage):
#         self.progress = self.total_progress * percentage
#         self.check_progress()
#
#     def check_progress(self):
#         if self.progress > self.total_progress:
#             self.progress = self.total_progress
#         elif self.progress < 0:
#             self.progress = 0
#
#     def display(self):
#         if self.progress != 0:
#             if self.horizontal:
#                 _Screen.rect(self.x, self.y, self.width * self.progress, self.height, self.color)
#             else:
#                 _Screen.rect(self.x, self.y, self.width, self.height * self.progress, self.color)
#
#
# class ProgressText(_TextDisplay):
#     def __init__(self, base, goal, ticks, x=0, y=0, characters="0123456789", font=None, pt=None, color=None,
#                  x_mode=_Al.df(), y_mode=_Al.df(), x_offset=0, y_offset=0, width=None, height=None):
#         self.base = base
#         self.goal = goal
#         self.ticks = ticks
#         self.progress = base
#         self.progress_per_tick = (self.goal - self.base) / self.ticks
#
#         _TextDisplay.__init__(self, x, y, characters, font, pt, color, x_mode, y_mode, x_offset, y_offset, width,
#                               height, self.progress)
#
#     def update_progress_per_tick(self):
#         self.progress_per_tick = (self.goal - self.base) / self.ticks
#
#     def set_progress(self, progress):
#         if progress < self.base:
#             self.progress = self.base
#         elif progress > self.goal:
#             self.progress = self.goal
#         else:
#             self.progress = progress
#
#     def set_base(self, base):
#         self.base = base
#         self.update_progress_per_tick()
#
#     def set_goal(self, goal):
#         self.goal = goal
#         self.update_progress_per_tick()
#
#     def set_ticks(self, ticks):
#         self.ticks = ticks
#         self.update_progress_per_tick()
#
#     def reset_progress(self):
#         self.progress = self.base
#
#     def reach_goal(self):
#         self.progress = self.goal
#         self.set_text(self.goal)
#
#     def update_text(self):
#         if self.progress < self.goal:
#             if self.progress + self.progress_per_tick <= self.goal:
#                 self.progress += self.progress_per_tick
#             else:
#                 self.progress = self.goal
#             self.set_text(int(self.progress))
#
#     def functions(self):
#         self.update_text()
#         self.display()
