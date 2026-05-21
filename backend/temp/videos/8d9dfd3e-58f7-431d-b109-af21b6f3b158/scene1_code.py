from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Create the Switch (Central Box)
        switch_rect = Rectangle(width=2.5, height=1.2, color=GOLD, fill_opacity=0.2)
        switch_label = Text("SWITCH", font_size=24, color=GOLD).move_to(switch_rect.get_center())
        switch = VGroup(switch_rect, switch_label).move_to(UP * 1)

        # 2. Create Computers A, B, C, D
        def create_pc(name, pos):
            pc_box = Square(side_length=0.8, color=BLUE, fill_opacity=0.1)
            pc_text = Text(name, font_size=24).move_to(pc_box.get_center())
            return VGroup(pc_box, pc_text).move_to(pos)

        pc_a = create_pc("A", [-4.5, 2.5, 0])
        pc_b = create_pc("B", [4.5, 2.5, 0])
        pc_c = create_pc("C", [-4.5, -0.5, 0])
        pc_d = create_pc("D", [4.5, -0.5, 0])

        # 3. Create Connections (Lines)
        line_a = Line(pc_a.get_center(), switch.get_center(), color=WHITE)
        line_b = Line(pc_b.get_center(), switch.get_center(), color=WHITE)
        line_c = Line(pc_c.get_center(), switch.get_center(), color=WHITE)
        line_d = Line(pc_d.get_center(), switch.get_center(), color=WHITE)
        connections = VGroup(line_a, line_b, line_c, line_d)

        # 4. Create MAC Address Table
        table_box = Rectangle(width=4, height=1.5, color=TEAL, fill_opacity=0.1)
        table_box.to_edge(DOWN, buff=0.5)
        table_header = Text("MAC Address Table", font_size=20, color=TEAL).next_to(table_box, UP, buff=0.1)
        entry1 = Text("Port 1: Address A", font_size=18).move_to(table_box.get_center() + UP * 0.3)
        entry2 = Text("Port 2: Address B", font_size=18).move_to(table_box.get_center() + DOWN * 0.3)
        mac_table = VGroup(table_box, table_header, entry1, entry2)

        # 5. Data Packet
        packet = Dot(color=RED, radius=0.15)
        packet.move_to(pc_a.get_center())

        # ANIMATION SEQUENCE
        # Show physical setup
        self.play(Create(switch), Create(pc_a), Create(pc_b), Create(pc_c), Create(pc_d))
        self.play(Create(connections))
        self.wait(1)

        # Show Table lookup logic
        self.play(Create(mac_table))
        self.wait(1)

        # Packet movement: A to Switch
        self.play(packet.animate.move_to(switch.get_center()), run_time=1.5)
        
        # Highlight logic: Table lookup for Address B
        self.play(entry2.animate.set_color(YELLOW), scale=1.2, run_time=0.5)
        self.play(entry2.animate.set_color(WHITE), run_time=0.5)

        # Packet movement: Switch to B
        self.play(packet.animate.move_to(pc_b.get_center()), run_time=1.5)
        
        # Cleanup/Final view
        self.play(packet.animate.scale(0), run_time=0.5)
        self.wait(2)