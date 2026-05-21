from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Title and Switch
        title = Text("Switch & MAC Directory", font_size=32).to_edge(UP)
        switch_box = Rectangle(color=BLUE, height=1.5, width=3, fill_opacity=0.3)
        switch_label = Text("SWITCH", font_size=24).move_to(switch_box.get_center())
        switch_group = VGroup(switch_box, switch_label).move_to(DOWN * 1)

        # 2. Nodes (Computers)
        node_a = VGroup(Square(side_length=0.8, color=TEAL), Text("A", font_size=24)).shift(LEFT * 4 + UP * 1)
        node_b = VGroup(Square(side_length=0.8, color=TEAL), Text("B", font_size=24)).shift(RIGHT * 4 + UP * 1)
        node_c = VGroup(Square(side_length=0.8, color=TEAL), Text("C", font_size=24)).shift(LEFT * 4 + DOWN * 3)
        node_d = VGroup(Square(side_length=0.8, color=TEAL), Text("D", font_size=24)).shift(RIGHT * 4 + DOWN * 3)

        # 3. Connections and Port Labels
        line_a = Line(node_a.get_right(), switch_box.get_left() + UP * 0.4)
        line_b = Line(node_b.get_left(), switch_box.get_right() + UP * 0.4)
        line_c = Line(node_c.get_right(), switch_box.get_left() + DOWN * 0.4)
        line_d = Line(node_d.get_left(), switch_box.get_right() + DOWN * 0.4)

        p1 = Text("P1", font_size=18).next_to(line_a.end, RIGHT, buff=0.1)
        p2 = Text("P2", font_size=18, color=YELLOW).next_to(line_b.end, LEFT, buff=0.1)
        p3 = Text("P3", font_size=18).next_to(line_c.end, RIGHT, buff=0.1)
        p4 = Text("P4", font_size=18).next_to(line_d.end, LEFT, buff=0.1)
        ports = VGroup(p1, p2, p3, p4)

        # 4. MAC Address Directory Table
        table_title = Text("MAC Address Directory", font_size=20, color=GOLD).move_to(UP * 2.8)
        table_header = VGroup(
            Rectangle(height=0.4, width=3, color=WHITE),
            Text("Port | MAC Address", font_size=18)
        ).next_to(table_title, DOWN, buff=0.1)
        
        row_highlight = Rectangle(height=0.4, width=3, color=YELLOW, fill_opacity=0.2).next_to(table_header, DOWN, buff=0)
        row_text = Text("Port 2 -> MAC B", font_size=18, color=YELLOW).move_to(row_highlight.get_center())
        row_b = VGroup(row_highlight, row_text)

        # 5. Animations
        self.play(Write(title))
        self.play(Create(switch_group), Create(VGroup(node_a, node_b, node_c, node_d)))
        self.wait(1)
        
        self.play(
            Create(VGroup(line_a, line_b, line_c, line_d)),
            Write(ports)
        )
        self.wait(1)

        self.play(FadeIn(table_title), Create(table_header))
        self.play(Write(row_b))
        
        # Highlight logic
        indicator_arrow = Arrow(row_highlight.get_right(), node_b.get_top(), color=YELLOW)
        self.play(Create(indicator_arrow))
        self.wait(2)

        # Final cleanup/outro
        self.play(
            FadeOut(indicator_arrow),
            row_highlight.animate.set_fill(YELLOW, opacity=0.5)
        )
        self.wait(2)