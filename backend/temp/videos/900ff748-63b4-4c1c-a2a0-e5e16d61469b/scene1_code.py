from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Central Switch Setup
        switch_rect = Rectangle(width=3.5, height=1.5, color=BLUE, fill_opacity=0.3)
        switch_label = Text("Layer 2 Switch", font_size=28).move_to(switch_rect.get_center())
        switch = VGroup(switch_rect, switch_label)

        # 2. PCs (Device Nodes)
        pc_a = VGroup(Circle(radius=0.4, color=WHITE, fill_opacity=0.2), Text("MAC A", font_size=18)).move_to([-4, 1.5, 0])
        pc_b = VGroup(Circle(radius=0.4, color=WHITE, fill_opacity=0.2), Text("MAC B", font_size=18)).move_to([4, 1.5, 0])
        pc_c = VGroup(Circle(radius=0.4, color=WHITE, fill_opacity=0.2), Text("MAC C", font_size=18)).move_to([-4, -1.5, 0])
        pc_d = VGroup(Circle(radius=0.4, color=WHITE, fill_opacity=0.2), Text("MAC D", font_size=18)).move_to([4, -1.5, 0])

        # 3. Connection Lines
        l1 = Line(switch_rect.get_left(), pc_a.get_right(), color=WHITE)
        l2 = Line(switch_rect.get_right(), pc_b.get_left(), color=WHITE)
        l3 = Line(switch_rect.get_left(), pc_c.get_right(), color=WHITE)
        l4 = Line(switch_rect.get_right(), pc_d.get_left(), color=WHITE)
        
        # Port labels next to lines
        p1_tag = Text("Port 1", font_size=14, color=GRAY).next_to(l1.get_start(), UP, buff=0.1)
        p3_tag = Text("Port 3", font_size=14, color=GRAY).next_to(l3.get_start(), DOWN, buff=0.1)

        # 4. MAC Directory (Table)
        table_box = Rectangle(width=4, height=2.2, color=TEAL, fill_opacity=0.1).to_edge(UP, buff=0.2)
        table_title = Text("MAC Directory Table", font_size=24, color=GOLD).next_to(table_box, UP, buff=0.1)
        
        row1 = Text("Port 1 : MAC A", font_size=20, color=YELLOW).move_to(table_box.get_top() + DOWN * 0.5)
        row2 = Text("Port 2 : MAC B", font_size=20).next_to(row1, DOWN, buff=0.15)
        row3 = Text("Port 3 : MAC C", font_size=20, color=YELLOW).next_to(row2, DOWN, buff=0.15)
        row4 = Text("Port 4 : MAC D", font_size=20).next_to(row3, DOWN, buff=0.15)
        
        mac_table = VGroup(table_box, table_title, row1, row2, row3, row4)

        # 5. Animations
        self.play(Create(switch), Create(pc_a), Create(pc_b), Create(pc_c), Create(pc_d))
        self.play(Create(l1), Create(l2), Create(l3), Create(l4), Write(p1_tag), Write(p3_tag))
        self.wait(1)

        self.play(Create(mac_table))
        self.play(row1.animate.scale(1.1), row3.animate.scale(1.1))
        self.wait(1)

        data_packet = VGroup(
            Rectangle(width=0.8, height=0.4, color=GOLD, fill_opacity=0.8),
            Text("Frame", font_size=14, color=BLACK).move_to(ORIGIN)
        ).move_to(switch.get_center())

        target_text = Text("Dest: MAC C", font_size=16, color=YELLOW).next_to(data_packet, UP, buff=0.1)

        self.play(FadeIn(data_packet), Write(target_text))
        
        self.play(
            data_packet.animate.move_to(pc_c.get_center()),
            target_text.animate.move_to(pc_c.get_center() + UP * 0.6),
            run_time=2.5,
            rate_func=smooth
        )
        
        # Fixed opacity keyword
        self.play(pc_c[0].animate.set_fill(YELLOW, fill_opacity=0.4))
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(data_packet), 
            FadeOut(target_text), 
            FadeOut(mac_table), 
            FadeOut(switch), 
            FadeOut(pc_a), 
            FadeOut(pc_b), 
            FadeOut(pc_c), 
            FadeOut(pc_d), 
            FadeOut(l1), 
            FadeOut(l2), 
            FadeOut(l3), 
            FadeOut(l4), 
            FadeOut(p1_tag), 
            FadeOut(p3_tag)
        )