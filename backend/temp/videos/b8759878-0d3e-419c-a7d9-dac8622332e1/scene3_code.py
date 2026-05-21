from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Title and Labels
        title = Text("Shared Bandwidth & Collision Domains", color=WHITE).scale(0.8)
        title.to_edge(UP, buff=0.5)

        logical_concept = Text("Logical Bus Topology", color=GOLD).scale(0.6)
        logical_concept.next_to(title, DOWN, buff=0.2)

        # 2. Central Hub
        hub_rect = Square(side_length=1.2, color=GOLD, fill_opacity=1.0)
        hub_text = Text("HUB", color=BLACK).scale(0.5).move_to(hub_rect.get_center())
        hub = VGroup(hub_rect, hub_text).move_to(ORIGIN)

        # 3. Stations (Computers)
        s1 = Circle(radius=0.4, color=BLUE, fill_opacity=0.8).move_to([-3, 1.5, 0])
        s2 = Circle(radius=0.4, color=BLUE, fill_opacity=0.8).move_to([3, 1.5, 0])
        s3 = Circle(radius=0.4, color=BLUE, fill_opacity=0.8).move_to([-3, -1.5, 0])
        s4 = Circle(radius=0.4, color=BLUE, fill_opacity=0.8).move_to([3, -1.5, 0])

        t1 = Text("PC A", color=WHITE).scale(0.3).next_to(s1, UP)
        t2 = Text("PC B", color=WHITE).scale(0.3).next_to(s2, UP)
        t3 = Text("PC C", color=WHITE).scale(0.3).next_to(s3, DOWN)
        t4 = Text("PC D", color=WHITE).scale(0.3).next_to(s4, DOWN)

        stations = VGroup(s1, s2, s3, s4, t1, t2, t3, t4)

        # 4. Connections
        l1 = Line(hub_rect.get_center(), s1.get_center(), color=WHITE)
        l2 = Line(hub_rect.get_center(), s2.get_center(), color=WHITE)
        l3 = Line(hub_rect.get_center(), s3.get_center(), color=WHITE)
        l4 = Line(hub_rect.get_center(), s4.get_center(), color=WHITE)
        lines = VGroup(l1, l2, l3, l4)

        # 5. Single Collision Domain Visual (The "Bubble")
        collision_domain = Rectangle(width=8.5, height=5.5, color=TEAL, fill_opacity=0.15)
        collision_domain.set_stroke(TEAL, 3)
        collision_label = Text("Single Collision Domain", color=TEAL).scale(0.7)
        collision_label.move_to(collision_domain.get_top() + DOWN * 0.4)
        domain_vgroup = VGroup(collision_domain, collision_label)

        # 6. Shared Bandwidth Status Bar
        bw_bg = Rectangle(width=6, height=0.4, color=WHITE).to_edge(DOWN, buff=0.8)
        bw_fill = Rectangle(width=6, height=0.4, color=YELLOW, fill_opacity=0.6).move_to(bw_bg.get_center())
        bw_label = Text("Shared Bandwidth (100%)", color=YELLOW).scale(0.5).next_to(bw_bg, UP, buff=0.1)
        bandwidth_vgroup = VGroup(bw_bg, bw_fill, bw_label)

        # 7. Animation Sequence
        self.play(Write(title))
        self.play(Create(hub), Create(stations), Create(lines))
        self.wait(1)
        
        self.play(Write(logical_concept))
        self.play(Create(domain_vgroup))
        self.wait(1)
        
        self.play(Create(bandwidth_vgroup))
        
        # Simulate shared bandwidth usage
        bw_div1 = Line(bw_bg.get_left() + RIGHT*1.5, bw_bg.get_left() + RIGHT*1.5 + UP*0.4, color=WHITE)
        bw_div2 = Line(bw_bg.get_left() + RIGHT*3.0, bw_bg.get_left() + RIGHT*3.0 + UP*0.4, color=WHITE)
        bw_div3 = Line(bw_bg.get_left() + RIGHT*4.5, bw_bg.get_left() + RIGHT*4.5 + UP*0.4, color=WHITE)
        
        self.play(
            Create(bw_div1), Create(bw_div2), Create(bw_div3),
            bw_label.animate.set_text("Bandwidth Split Across Ports")
        )
        
        self.wait(2)