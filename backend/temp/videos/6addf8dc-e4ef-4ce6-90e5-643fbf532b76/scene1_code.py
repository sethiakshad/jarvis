from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Create Switch and PCs
        switch_box = Rectangle(height=1.5, width=3, color=BLUE, fill_opacity=0.5)
        switch_label = Text("Switch", font_size=24).move_to(switch_box.get_center())
        switch_group = VGroup(switch_box, switch_label)

        pc_a = Square(side_length=1.0, color=TEAL, fill_opacity=0.3).move_to([-4, 2, 0])
        label_a = Text("A", font_size=20).move_to(pc_a.get_center())
        pc_b = Square(side_length=1.0, color=TEAL, fill_opacity=0.3).move_to([-4, -2, 0])
        label_b = Text("B", font_size=20).move_to(pc_b.get_center())
        pc_c = Square(side_length=1.0, color=TEAL, fill_opacity=0.3).move_to([4, 2, 0])
        label_c = Text("C", font_size=20).move_to(pc_c.get_center())
        pc_d = Square(side_length=1.0, color=TEAL, fill_opacity=0.3).move_to([4, -2, 0])
        label_d = Text("D", font_size=20).move_to(pc_d.get_center())

        # Connections
        line_a = Line(pc_a.get_right(), switch_box.get_left(), color=WHITE)
        line_b = Line(pc_b.get_right(), switch_box.get_left(), color=WHITE)
        line_c = Line(pc_c.get_left(), switch_box.get_right(), color=WHITE)
        line_d = Line(pc_d.get_left(), switch_box.get_right(), color=WHITE)

        # Labels for ports
        p1 = Text("P1", font_size=16).next_to(switch_box.get_left(), RIGHT, buff=0.1).shift(UP * 0.3)
        p3 = Text("P3", font_size=16).next_to(switch_box.get_right(), LEFT, buff=0.1).shift(UP * 0.3)

        # 2. MAC Table - Using Text instead of MathTex to avoid LaTeX subprocess errors
        table_rect = Rectangle(height=1.5, width=3.5, color=WHITE, fill_opacity=0.1).to_edge(UP)
        table_header = Text("Port | Address", font_size=24).move_to(table_rect.get_top() + DOWN * 0.3)
        table_row1 = Text("1     A", font_size=24, color=YELLOW).next_to(table_header, DOWN, buff=0.2)
        table_row2 = Text("3     C", font_size=24, color=YELLOW).next_to(table_row1, DOWN, buff=0.1)
        table_group = VGroup(table_rect, table_header, table_row1, table_row2)

        # 3. Animations Start
        self.play(Create(switch_group), Create(VGroup(pc_a, label_a, pc_b, label_b, pc_c, label_c, pc_d, label_d)))
        self.play(Create(VGroup(line_a, line_b, line_c, line_d, p1, p3)))
        self.wait(1)
        
        self.play(Write(table_group))
        self.wait(1)

        # 4. Packet Animation
        packet = Rectangle(height=0.3, width=0.5, color=GOLD, fill_opacity=1)
        packet_label = Text("Data", font_size=12, color=BLACK).move_to(packet.get_center())
        packet_vg = VGroup(packet, packet_label).move_to(pc_a.get_center())

        # Path: PC A -> Switch -> PC C
        self.play(packet_vg.animate.move_to(switch_box.get_center()), run_time=2)
        
        # Highlight the lookup in the table
        self.play(table_row2.animate.set_color(GREEN).scale(1.2))
        self.play(table_row2.animate.set_color(YELLOW).scale(1/1.2))

        # Packet moves specifically to Port 3 -> PC C
        self.play(packet_vg.animate.move_to(pc_c.get_center()), run_time=2)
        
        # Success highlight
        success_rect = Square(side_length=1.2, color=GREEN).move_to(pc_c.get_center())
        self.play(Create(success_rect))
        self.play(FadeOut(success_rect))
        
        self.wait(2)