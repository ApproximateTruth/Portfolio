from manim import *
from manim.utils.rate_functions import *


# Date Created 11/07/21
# Last Updated 14/07/21
# This animations serves as the waiting screen before streams or during breaks of streams
# This was created with the kind help of and using examples from https://www.manim.community/
# TODO: FIX OUTLINE HAVING A LINE STICKING UP AT THE TOP, Priority: High
# TODO: DEALING WITH NDARRY EXPECTATIONS, Priority: Medium
# TODO: TRIPLE CHECK COLOR CHOICES, Priority: Low
# TODO: EXPERIMENT WITH INCREASING THE CYCLE TIME BETWEEN CYCLES BY [run_time=15 + color_num], Priority: Low


class WaitingScreen(Scene):
    def construct(self):
        # This bock initializes many of the geometry used in the path finding for the animation
        path_0 = Circle(radius=3.8).rotate(PI / 2)
        # These are segment arcs which are paths with different starting locations by having different lengths
        path_1, path_2, path_3, path_4, path_5, path_6, path_7, path_8, path_9, path_10, path_11 = (
            Arc(angle=((PI / 6) * 1), radius=3.8), Arc(angle=((PI / 6) * 2), radius=3.8),
            Arc(angle=((PI / 6) * 3), radius=3.8), Arc(angle=((PI / 6) * 4), radius=3.8),
            Arc(angle=((PI / 6) * 5), radius=3.8), Arc(angle=((PI / 6) * 6), radius=3.8),
            Arc(angle=((PI / 6) * 7), radius=3.8), Arc(angle=((PI / 6) * 8), radius=3.8),
            Arc(angle=((PI / 6) * 9), radius=3.8), Arc(angle=((PI / 6) * 10), radius=3.8),
            Arc(angle=((PI / 6) * 11), radius=3.8)
        )
        dot_0 = Dot().shift(UP * 3.78)
        # These are the dots used
        dot_1, dot_2, dot_3, dot_4, dot_5, dot_6, dot_7, dot_8, dot_9, dot_10, dot_11 = (
            Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot(), Dot()
        )
        d_group = VGroup(dot_0, dot_1, dot_2, dot_3, dot_4, dot_5, dot_6, dot_7, dot_8, dot_9, dot_10, dot_11)
        a_group = VGroup(path_1, path_2, path_3, path_4, path_5, path_6, path_7, path_8, path_9, path_10, path_11)
        d_group.set_color(BLUE)
        # This rotation is so that the starting end of all arc segments is at the top of the circle outline
        a_group.rotate(4 * PI / 6, about_point=[0, 0, 0])
        message = Text("Stream Will Begin Shortly").scale(0.9)
        c_deck = [PURPLE_B, BLUE, GREEN, YELLOW, ORANGE, RED_D]
        box = SurroundingRectangle(message, color=RED)

        # The Waiting function is where the actual animation is kept and so it can be called with different features

        def waiting(color_num):
            outline = VMobject()
            # The color for the dots and outline is meant to be the opposite of that of the box surronding the text
            d_group.set_color(c_deck[color_num])
            box.set_color(c_deck[5 - color_num])
            # This section animates the flash along with the appear box around the main text
            self.play(Flash(message, num_lines=12, color=c_deck[5 - color_num], rate_func=rush_from, flash_radius=3.8),
                      FadeIn(box)
                      )
            self.play(FadeOut(box, run_time=1.2))
            self.wait(0.5)
            self.play(FadeIn(dot_0))
            # This section animates the top dot moving in a circle to "place" dots in a circle.
            j = 1
            while j < 13:
                self.play(dot_0.animate(rate_func=smooth).rotate(PI / 6, about_point=[0, 0, 0]))
                d_group[12 - j].shift(dot_0.get_center())
                self.add(d_group[12 - j])
                j += 1
            # This sections creates the updating function for the outline and defines what values to update
            outline.set_points_as_corners([dot_0.get_center(), dot_0.get_center()])

            def circleoutline(outline_0):
                prime = outline_0.copy()
                prime.add_points_as_corners([dot_0.get_center()])
                outline.become(prime.set_color(c_deck[color_num]))

            outline.add_updater(circleoutline)
            self.add(outline)
            # This section animates the 12 dotes moving in a circle to meet up at the top in the run time
            self.play(
                MoveAlongPath(dot_0, path_0, run_time=15, rate_func=linear),
                MoveAlongPath(dot_1, path_1, run_time=15, rate_func=linear),
                MoveAlongPath(dot_2, path_2, run_time=15, rate_func=linear),
                MoveAlongPath(dot_3, path_3, run_time=15, rate_func=linear),
                MoveAlongPath(dot_4, path_4, run_time=15, rate_func=linear),
                MoveAlongPath(dot_5, path_5, run_time=15, rate_func=linear),
                MoveAlongPath(dot_6, path_6, run_time=15, rate_func=linear),
                MoveAlongPath(dot_7, path_7, run_time=15, rate_func=linear),
                MoveAlongPath(dot_8, path_8, run_time=15, rate_func=linear),
                MoveAlongPath(dot_9, path_9, run_time=15, rate_func=linear),
                MoveAlongPath(dot_10, path_10, run_time=15, rate_func=linear),
                MoveAlongPath(dot_11, path_11, run_time=15, rate_func=linear),
            )
            self.play(FadeOut(d_group))
            # This section resets the dots posistions such that when they are called they are placed correctly.
            L = 1
            while L < 13:
                d_group[12 - L].move_to([0, 0, 0])
                L += 1
            dot_0.shift(UP * 3.8)
            self.play(FadeOut(outline, scale=1.5))
            # Resets the updater function
            self.remove(outline)
            outline.remove_updater(circleoutline)

        # This section writes the text of the screen
        self.play(Write(message))
        self.wait(0.5)
        # This section rotates all arc segments such that their tips end at the 12 hour mark on the circle
        i = 0
        while i < 12:
            a_group[i - 1].rotate((11 - i) * (PI / 6), about_point=[0, 0, 0])
            i += 1

        # This section runs the animation cycle over the different colors
        k = 0
        while k < 6:
            waiting(k)
            k += 1
        # END OF PROGRAM
        self.play(Unwrite(message))
        self.wait(1.5)
