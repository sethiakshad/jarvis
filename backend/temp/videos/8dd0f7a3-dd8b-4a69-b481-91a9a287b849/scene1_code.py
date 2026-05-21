from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Setup the Switch
        switch_rect = Rectangle(width=3, height=2, color=BLUE, fill_opacity=0.3)
        switch_label = Text("Switch", color=WHITE).scale(0.8)
        switch = VGroup(switch_rect, switch_label).move_to(2 * LEFT)

        # 2. Setup Devices (A, B, C, D)
        dev_a = VGroup(Square(side_length=0.7, color=TEAL, fill_opacity=0.6), Text("A", font_size=24)).move_to([-5, 1.5, 0])
        dev_b = VGroup(Square(side_length=0.7, color=TEAL, fill_opacity=0.6), Text("B", font_size=24)).move_to([-5, -1.5, 0])
        dev_c = VGroup(Square(side_length=0.7, color=TEAL, fill_opacity=0.6), Text("C", font_size=24)).move_to([1, 1.5, 0])
        dev_d = VGroup(Square(side_length=0.7, color=TEAL, fill_opacity=0.6), Text("D", font_size=24)).move_to([1, -1.5, 0])

        # 3. Ports and Connections
        p1_pos = switch_rect.get_left() + UP * 0.5
        p2_pos = switch_rect.get_left() + DOWN * 0.5
        p3_pos = switch_rect.get_right() + UP * 0.5
        p4_pos = switch_rect.get_right() + DOWN * 0.5

        line_a = Line(dev_a.get_right(), p1_pos, color=WHITE)
        line_b = Line(dev_b.get_right(), p2_pos, color=WHITE)
        line_c = Line(dev_c.get_left(), p3_pos, color=WHITE)
        line_d = Line(dev_d.get_left(), p4_pos, color=WHITE)

        # 4. Port Directory Table
        table_box = Rectangle(width=3.2, height=3, color=GOLD, fill_opacity=0.1)
        table_title = Text("Directory Table", font_size=22, color=GOLD).next_to(table_box.get_top(), DOWN, buff=0.2)
        row1 = Text("Port 1: Addr A", font_size=18).move_to(table_box.get_center() + UP * 0.4)
        row2 = Text("Port 2: Addr B", font_size=18).next_to(row1, DOWN, buff=0.15)
        row3 = Text("Port 3: Addr C", font_size=18).next_to(row2, DOWN, buff=0.15)
        row4 = Text("Port 4: Addr D", font_size=18).next_to(row3, DOWN, buff=0.15)
        table = VGroup(table_box, table_title, row1, row2, row3, row4).to_edge(RIGHT, buff=0.5)

        # 5. Packet
        packet = Circle(radius=0.12, color=RED, fill_opacity=1)
        packet.move_to(dev_a.get_center())

        # Animations
        self.play(Write(switch), Write(VGroup(dev_a, dev_b, dev_c, dev_d)))
        self.play(Create(line_a), Create(line_b), Create(line_c), Create(line_d))
        self.wait(1)
        
        self.play(Write(table))
        self.wait(1)

        # Data Movement sequence: A -> Port 1 -> Port 3 -> C
        self.play(packet.animate.move_to(p1_pos), run_time=1.5)
        self.play(Indicate(row1, color=YELLOW), Indicate(row3, color=YELLOW))
        self.play(packet.animate.move_to(p3_pos), run_time=1.5)
        self.play(packet.animate.move_to(dev_c.get_center()), run_time=1.5)
        
        self.play(FadeOut(packet))
        self.wait(2)