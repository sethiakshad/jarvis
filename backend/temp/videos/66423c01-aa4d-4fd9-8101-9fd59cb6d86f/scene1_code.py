from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Create the central Switch
        switch_box = Rectangle(width=2.5, height=1.2, color=BLUE, fill_opacity=0.8)
        switch_label = Text("Switch", font_size=24, color=WHITE).move_to(switch_box.get_center())
        switch_group = VGroup(switch_box, switch_label).move_to(ORIGIN)

        # 2. Create the Computers
        pc_a = Square(side_length=0.8, color=WHITE, fill_opacity=0.2).move_to([-4, 2, 0])
        pc_b = Square(side_length=0.8, color=WHITE, fill_opacity=0.2).move_to([4, 2, 0])
        pc_c = Square(side_length=0.8, color=WHITE, fill_opacity=0.2).move_to([-4, -2, 0])
        pc_d = Square(side_length=0.8, color=WHITE, fill_opacity=0.2).move_to([4, -2, 0])

        label_a = Text("A", font_size=20).next_to(pc_a, UP)
        label_b = Text("B", font_size=20).next_to(pc_b, UP)
        label_c = Text("C", font_size=20).next_to(pc_c, DOWN)
        label_d = Text("D", font_size=20).next_to(pc_d, DOWN)

        computers = VGroup(pc_a, pc_b, pc_c, pc_d, label_a, label_b, label_c, label_d)

        # 3. Create Connection Lines
        line_a = Line(pc_a.get_center(), switch_box.get_center(), color=WHITE, stroke_width=2)
        line_b = Line(pc_b.get_center(), switch_box.get_center(), color=WHITE, stroke_width=2)
        line_c = Line(pc_c.get_center(), switch_box.get_center(), color=WHITE, stroke_width=2)
        line_d = Line(pc_d.get_center(), switch_box.get_center(), color=WHITE, stroke_width=2)
        lines = VGroup(line_a, line_b, line_c, line_d)

        # 4. Create Address Table
        table_bg = Rectangle(width=2.5, height=1.8, color=GOLD, fill_opacity=0.9).to_edge(UP, buff=0.3)
        table_title = Text("Address Table", font_size=18, color=BLACK).move_to(table_bg.get_top() + DOWN * 0.3)
        table_data = Text("P1: A\nP2: B\nP3: C\nP4: D", font_size=16, color=BLACK, line_spacing=0.8).next_to(table_title, DOWN, buff=0.1)
        table_group = VGroup(table_bg, table_title, table_data)

        # 5. Display Initial Network
        self.play(Create(lines), Create(switch_group), Create(computers))
        self.wait(1)
        self.play(Create(table_group))
        self.wait(1)

        # 6. Data Packet Animation
        packet_shape = Rectangle(width=0.8, height=0.4, color=TEAL, fill_opacity=1)
        packet_text = Text("For B", font_size=14, color=WHITE).move_to(packet_shape.get_center())
        packet = VGroup(packet_shape, packet_text).move_to(pc_a.get_center())

        # Animate packet from PC A to Switch
        self.play(packet.animate.move_to(switch_box.get_center()), run_time=2)
        
        # Highlight Port 2 in the table
        highlight_rect = Rectangle(width=2.2, height=0.3, color=RED, stroke_width=2).move_to(table_data.get_top() + DOWN * 0.5)
        self.play(Create(highlight_rect))
        self.wait(0.5)
        self.play(FadeOut(highlight_rect))

        # Animate packet from Switch to PC B
        self.play(packet.animate.move_to(pc_b.get_center()), run_time=2)
        self.wait(2)

        # Final Cleanup
        self.play(FadeOut(packet), FadeOut(table_group), FadeOut(computers), FadeOut(switch_group), FadeOut(lines))