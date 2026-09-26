"""S09 - Homomorphic addition: add ciphertexts, and the noise adds too.

Adding the two ciphertext components adds the messages - but the noise budgets
add as well, so only a limited number of additions are safe.

The bar is measured, not drawn by hand. MEDIAN_NOISE[n - 1] is the median of the
largest |noise coefficient| over 20,000 sums of n fresh ciphertexts, and FAIL_PCT
the share of those sums whose noise passes the budget q/(2t) = 874/14 = 62.4, both
from combined_noise() in code/noise_plots.py (d 16, t 7, q 874, sigma 1.5, seed
1234). The median first passes the budget at 20 additions.
"""

from manim import *

from theme import MSG, NOISE

BUDGET = 874 / (2 * 7)
MEDIAN_NOISE = [14, 20, 25, 28, 32, 35, 38, 40, 43, 45,
                47, 49, 51, 53, 55, 57, 59, 60, 62, 64]
FAIL_PCT = [0.0, 0.0, 0.0, 0.07, 0.35, 0.95, 2.27, 4.34, 6.88, 9.96,
            13.58, 18.04, 23.0, 26.56, 31.39, 35.61, 40.02, 44.76, 48.97, 53.12]


class HomAddNoise(Scene):
    def construct(self):
        title = Text("Homomorphic addition", font_size=40).to_edge(UP)
        self.play(Write(title))

        line = MathTex(
            r"E(m_1) + E(m_2)", r"=", r"E(m_1 + m_2)", font_size=48
        ).next_to(title, DOWN, buff=0.6)
        line[0].set_color(MSG)
        line[2].set_color(MSG)
        self.play(Write(line[0]))
        self.play(Write(line[1]), Write(line[2]))
        note = Text("add componentwise; the message just adds", font_size=25, color=MSG)
        note.next_to(line, DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(0.8)

        # Noise budget bar filling as additions accumulate
        bar_bg = RoundedRectangle(width=8.0, height=0.7, corner_radius=0.1, color=GREY_B)
        bar_bg.next_to(note, DOWN, buff=1.0)
        budget_line = DashedLine(bar_bg.get_corner(UR), bar_bg.get_corner(DR), color=WHITE)
        budget_lbl = MathTex(r"q/(2t)", font_size=30).next_to(bar_bg, RIGHT, buff=0.2)
        self.play(Create(bar_bg), Create(budget_line), FadeIn(budget_lbl))

        counter = Integer(0, font_size=40).next_to(bar_bg, UP, buff=0.35)
        counter_lbl = Text("ciphertexts added", font_size=22).next_to(counter, RIGHT, buff=0.25)
        fail = DecimalNumber(0, num_decimal_places=1, unit=r"\%", font_size=32)
        fail.next_to(bar_bg, DOWN, buff=0.35).align_to(bar_bg, LEFT)
        fail_lbl = Text("of decryptions fail", font_size=22).next_to(fail, RIGHT, buff=0.2)
        # Keep each label clear of its number as the number gains digits.
        counter_lbl.add_updater(lambda m: m.next_to(counter, RIGHT, buff=0.25))
        fail_lbl.add_updater(lambda m: m.next_to(fail, RIGHT, buff=0.2))
        self.play(FadeIn(counter), FadeIn(counter_lbl), FadeIn(fail), FadeIn(fail_lbl))

        fill = Rectangle(width=0.01, height=0.7, color=NOISE, fill_opacity=0.8)
        fill.align_to(bar_bg, LEFT).set_y(bar_bg.get_y())
        self.add(fill)

        for i, (noise, pct) in enumerate(zip(MEDIAN_NOISE, FAIL_PCT), start=1):
            over = noise > BUDGET
            target = Rectangle(width=8.0 * min(noise / BUDGET, 1.0), height=0.7,
                               color=YELLOW if over else NOISE, fill_opacity=0.8)
            target.align_to(bar_bg, LEFT).set_y(bar_bg.get_y())
            self.play(Transform(fill, target), ChangeDecimalToValue(counter, i),
                      ChangeDecimalToValue(fail, pct), run_time=0.4)

        warn = Text("the typical noise passes the budget: about half of decryptions fail",
                    font_size=24, color=YELLOW).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(warn))
        self.wait(1.6)
