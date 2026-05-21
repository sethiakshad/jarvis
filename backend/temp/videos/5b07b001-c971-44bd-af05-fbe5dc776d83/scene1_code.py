from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Create the central Switch
        switch_body = Rectangle(width=4, height=2.5, color=BLUE, fill_opacity=0.3)
        switch_body.move_to(DOWN * 0.5)
        switch_label = Text("Ethernet Switch", color=WHITE, font_size=28).move_to(switch_body.get_center())
        switch_group = VGroup(switch_body, switch_label)

        # 2. Create Ports and their labels
        port_size = 0.6
        p1 = Square(side_length=port_size, color=WHITE, fill_opacity=0.1).move_to([-4, 0.5, 0])
        p2 = Square(side_length=port_size, color=WHITE, fill_opacity=0.1).move_to([-4, -1.5, 0])
        p3 = Square(side_length=port_size, color=WHITE, fill_opacity=0.1).move_to([4, 0.5, 0])
        p4 = Square(side_length=port_size, color=WHITE, fill_opacity=0.1).move_to([4, -1.5, 0])
        
        l1 = Text("Port 1", font_size=20).next_to(p1, LEFT)
        l2 = Text("Port 2", font_size=20).next_to(p2, LEFT)
        l3 = Text("Port 3", font_size=20).next_to(p3, RIGHT)
        l4 = Text("Port 4", font_size=20).next_to(p4, RIGHT)
        
        ports = VGroup(p1, p2, p3, p4)
        port_labels = VGroup(l1, l2, l3, l4)

        # 3. Connections
        conn1 = Line(p1.get_right(), switch_body.get_left() + UP * 1.0, color=GRAY)
        conn2 = Line(p2.get_right(), switch_body.get_left() + DOWN * 1.0, color=GRAY)
        conn3 = Line(p3.get_left(), switch_body.get_right() + UP * 1.0, color=GRAY)
        conn4 = Line(p4.get_left(), switch_body.get_right() + DOWN * 1.0, color=GRAY)
        connections = VGroup(conn1, conn2, conn3, conn4)

        # 4. Directory Table (Hidden initially)
        table_bg = Rectangle(width=5, height=1.5, color=TEAL, fill_opacity=0.2).to_edge(UP, buff=0.5)
        table_title = Text("MAC Address Table", font_size=22, color=YELLOW).move_to(table_bg.get_top() + DOWN * 0.3)
        table_entry = MathTex(r"\text{Port 3} \longleftrightarrow \text{MAC Address B}", font_size=30).move_to(table_bg.get_center() + DOWN * 0.2)
        table_group = VGroup(table_bg, table_title, table_entry)

        # 5. Data Frame
        frame = Rectangle(width=0.8, height=0.5, color=GOLD, fill_opacity=1)
        frame_text = Text("Data", font_size=16, color=BLACK).move_to(frame.get_center())
        frame_vgroup = VGroup(frame, frame_text)
        frame_vgroup.move_to([-6, 0.5, 0])

        # Animation Sequence
        self.play(Create(switch_group), Create(ports), Create(connections), Write(port_labels))
        self.wait(1)

        # Frame arrives at Port 1
        self.play(frame_vgroup.animate.move_to(p1.get_center()), run_time=1.5)
        self.wait(0.5)

        # Move to switch center and show table
        self.play(
            frame_vgroup.animate.move_to(switch_body.get_center()),
            FadeIn(table_group),
            run_time=2
        )
        self.wait(2)

        # Identification Highlight
        rect_highlight = Rectangle(width=5.2, height=0.6, color=RED).move_to(table_entry.get_center())
        self.play(Create(rect_highlight))
        self.play(FadeOut(rect_highlight))

        # Forwarding to Port 3
        self.play(frame_vgroup.animate.move_to(p3.get_center()), run_time=1.5)
        self.wait(0.5)

        # Exit
        self.play(
            frame_vgroup.animate.move_to([6, 0.5, 0]),
            FadeOut(table_group),
            run_time=2
        )
        self.wait(1)