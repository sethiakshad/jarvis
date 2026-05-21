from manim import *

class Scene2(Scene):
    def construct(self):
        # 1. Setup the Switch and Nodes
        switch_rect = Rectangle(width=4, height=2, color=BLUE, fill_opacity=0.2)
        switch_label = Text("SWITCH", color=BLUE).scale(0.8)
        switch_group = VGroup(switch_rect, switch_label).move_to(ORIGIN)

        node_a = Circle(radius=0.4, color=WHITE, fill_opacity=0.5).shift(LEFT * 5 + UP * 2)
        node_b = Circle(radius=0.4, color=WHITE, fill_opacity=0.5).shift(LEFT * 5 + DOWN * 2)
        node_c = Circle(radius=0.4, color=WHITE, fill_opacity=0.5).shift(RIGHT * 5 + UP * 2)
        node_d = Circle(radius=0.4, color=WHITE, fill_opacity=0.5).shift(RIGHT * 5 + DOWN * 2)

        label_a = Text("A", color=WHITE).scale(0.6).move_to(node_a)
        label_b = Text("B", color=WHITE).scale(0.6).move_to(node_b)
        label_c = Text("C", color=WHITE).scale(0.6).move_to(node_c)
        label_d = Text("D", color=WHITE).scale(0.6).move_to(node_d)

        line_a = Line(node_a.get_right(), switch_rect.get_left(), color=GRAY)
        line_b = Line(node_b.get_right(), switch_rect.get_left(), color=GRAY)
        line_c = Line(node_c.get_left(), switch_rect.get_right(), color=GRAY)
        line_d = Line(node_d.get_left(), switch_rect.get_right(), color=GRAY)

        nodes = VGroup(node_a, node_b, node_c, node_d, label_a, label_b, label_c, label_d)
        lines = VGroup(line_a, line_b, line_c, line_d)

        self.play(Create(switch_group), Create(nodes), Create(lines))
        self.wait(1)

        # 2. MAC Address Table
        table_bg = Rectangle(width=3, height=2, color=GOLD, fill_opacity=0.1).to_edge(UP)
        table_title = Text("MAC Table", color=GOLD).scale(0.5).next_to(table_bg, UP, buff=0.1)
        table_content = MathTex(
            r"\text{Port 1} \rightarrow A \\ \text{Port 3} \rightarrow C", 
            color=WHITE
        ).scale(0.7).move_to(table_bg.get_center())
        mac_table = VGroup(table_bg, table_title, table_content)

        self.play(Create(mac_table))
        self.wait(1)

        # 3. Data Transfer Animation
        data_packet = Dot(color=YELLOW).move_to(node_a.get_center())
        target_info = Text("To: Node C", color=YELLOW).scale(0.4).next_to(data_packet, UP)

        self.play(FadeIn(data_packet), Write(target_info))
        
        # Move to switch
        self.play(
            data_packet.animate.move_to(switch_rect.get_center()),
            target_info.animate.move_to(switch_rect.get_top() + UP*0.3),
            run_time=1.5
        )

        # Highlight Table lookup
        highlight_box = Rectangle(width=2.8, height=0.4, color=YELLOW).move_to(table_content[0][6:13])
        self.play(Create(highlight_box))
        self.wait(0.5)

        # Direct forwarding
        self.play(
            data_packet.animate.move_to(node_c.get_center()),
            FadeOut(target_info),
            run_time=1.5
        )
        
        # Efficiency Indicators
        idle_b = Text("Idle", color=GREEN).scale(0.4).next_to(node_b, RIGHT)
        idle_d = Text("Idle", color=GREEN).scale(0.4).next_to(node_d, LEFT)
        efficiency_text = Text("No Collision: Targeted Delivery", color=TEAL).scale(0.6).to_edge(DOWN)

        self.play(Write(idle_b), Write(idle_d), Write(efficiency_text))
        self.play(Flash(node_c, color=YELLOW))
        
        self.wait(2)
        
        # Cleanup
        self.play(
            FadeOut(nodes), 
            FadeOut(lines), 
            FadeOut(switch_group), 
            FadeOut(mac_table), 
            FadeOut(data_packet),
            FadeOut(idle_b),
            FadeOut(idle_d),
            FadeOut(efficiency_text),
            FadeOut(highlight_box)
        )