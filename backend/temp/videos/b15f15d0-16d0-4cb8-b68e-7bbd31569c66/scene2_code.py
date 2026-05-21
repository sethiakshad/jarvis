from manim import *

class Scene2(Scene):
    def construct(self):
        # Title
        title = Text("Switch: The Intelligent Bridge", color=BLUE, font_size=36).to_edge(UP)
        
        # Central Switch
        switch_rect = Rectangle(width=3, height=1.5, color=GOLD, fill_opacity=0.3)
        switch_text = Text("Switch", font_size=24).move_to(switch_rect.get_center())
        switch = VGroup(switch_rect, switch_text)
        
        # MAC Table Overlay
        table_box = Rectangle(width=2.2, height=1.5, color=WHITE, fill_opacity=0.15).next_to(switch, UP, buff=0.5)
        table_title = Text("MAC Table", font_size=18, color=TEAL).move_to(table_box.get_top() + DOWN * 0.25)
        table_data = Text("PC-A: Port 1\nPC-B: Port 2", font_size=16).next_to(table_title, DOWN, buff=0.2)
        mac_table = VGroup(table_box, table_title, table_data)

        # Connected PCs
        pc_a = VGroup(Square(side_length=0.8, color=BLUE, fill_opacity=0.2), Text("PC-A", font_size=18)).next_to(switch, LEFT, buff=2)
        pc_b = VGroup(Square(side_length=0.8, color=BLUE, fill_opacity=0.2), Text("PC-B", font_size=18)).next_to(switch, RIGHT, buff=2).shift(UP * 1)
        pc_c = VGroup(Square(side_length=0.8, color=BLUE, fill_opacity=0.2), Text("PC-C", font_size=18)).next_to(switch, RIGHT, buff=2).shift(DOWN * 1)
        
        # Physical Connections (Lines)
        line_a = Line(pc_a.get_right(), switch_rect.get_left(), color=WHITE)
        line_b = Line(switch_rect.get_right(), pc_b.get_left(), color=WHITE)
        line_c = Line(switch_rect.get_right(), pc_c.get_left(), color=WHITE)
        connections = VGroup(line_a, line_b, line_c)
        
        # Packet
        packet = Dot(color=YELLOW, radius=0.15)
        packet_label = Text("Data", font_size=14, color=YELLOW).next_to(packet, UP, buff=0.1)
        data_packet = VGroup(packet, packet_label).move_to(pc_a.get_center())

        # Explanatory Label
        info_text = Text("Direct Forwarding via MAC Table", color=GREEN, font_size=22).to_edge(DOWN)

        # Animation Sequence
        self.play(Write(title))
        self.play(Create(switch), Create(pc_a), Create(pc_b), Create(pc_c))
        self.play(Create(connections))
        self.wait(1)
        
        self.play(Create(mac_table))
        self.wait(1)

        # Packet movement: PC-A to Switch
        self.play(data_packet.animate.move_to(switch.get_center()), run_time=1.5)
        
        # Visual cue for "Looking up table"
        self.play(table_box.animate.set_color(YELLOW), run_time=0.4)
        self.play(table_box.animate.set_color(WHITE), run_time=0.4)
        
        # Forwarding to PC-B only (PC-C remains idle)
        self.play(
            data_packet.animate.move_to(pc_b.get_center()),
            Write(info_text),
            run_time=1.5
        )
        
        # Highlighting Dedicated Bandwidth concept
        bw_box = Rectangle(width=3, height=0.6, color=RED).move_to(line_b.get_center())
        bw_text = Text("Dedicated Bandwidth", font_size=14, color=RED).next_to(bw_box, UP, buff=0.1)
        
        self.play(Create(bw_box), Write(bw_text))
        self.wait(2)

        # Final state check: PC-C path was never used
        idle_label = Text("Idle / No Collision", font_size=16, color=WHITE).next_to(line_c, DOWN, buff=0.2)
        self.play(Write(idle_label))
        self.wait(2)