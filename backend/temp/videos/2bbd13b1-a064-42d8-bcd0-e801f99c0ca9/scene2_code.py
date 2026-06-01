from manim import *

class Scene2(Scene):
    def construct(self):
        # 1. Create Smartphone Representation
        phone_body = Rectangle(height=5, width=2.6, color=WHITE, fill_opacity=0.1)
        phone_screen = Rectangle(height=4, width=2.4, color=WHITE, fill_opacity=0.2).move_to(phone_body.get_center())
        home_button = Circle(radius=0.15, color=WHITE).next_to(phone_screen, DOWN, buff=0.2)
        phone = VGroup(phone_body, phone_screen, home_button)

        # 2. Define Feature Nodes
        sqlite_node = Circle(radius=0.7, color=BLUE, fill_opacity=0.4)
        sqlite_text = Text("SQLite", font_size=20).move_to(sqlite_node.get_center())
        sqlite = VGroup(sqlite_node, sqlite_text).next_to(phone, LEFT, buff=1).shift(UP * 1.5)

        nfc_node = Circle(radius=0.7, color=TEAL, fill_opacity=0.4)
        nfc_text = Text("NFC", font_size=20).move_to(nfc_node.get_center())
        nfc = VGroup(nfc_node, nfc_text).next_to(phone, RIGHT, buff=1).shift(UP * 1.5)

        touch_node = Circle(radius=0.7, color=GOLD, fill_opacity=0.4)
        touch_text = Text("Multi-touch", font_size=18).move_to(touch_node.get_center())
        touch_feat = VGroup(touch_node, touch_text).next_to(phone, DOWN, buff=0.4)

        # 3. Define Multi-touch Visuals (Fingers)
        finger1 = Dot(point=phone_screen.get_center() + UP * 0.8 + LEFT * 0.4, color=RED, radius=0.18)
        finger2 = Dot(point=phone_screen.get_center() + DOWN * 0.8 + RIGHT * 0.4, color=RED, radius=0.18)
        fingers = VGroup(finger1, finger2)

        # 4. Animation Sequence
        self.play(Create(phone), run_time=1.5)
        self.play(
            Create(sqlite), 
            Create(nfc), 
            Create(touch_feat), 
            run_time=2
        )
        self.wait(1)

        # Pulse effect for the nodes
        self.play(
            sqlite_node.animate.scale(1.2).set_fill(opacity=0.6),
            nfc_node.animate.scale(1.2).set_fill(opacity=0.6),
            touch_node.animate.scale(1.2).set_fill(opacity=0.6),
            run_time=1
        )
        self.play(
            sqlite_node.animate.scale(1/1.2).set_fill(opacity=0.4),
            nfc_node.animate.scale(1/1.2).set_fill(opacity=0.4),
            touch_node.animate.scale(1/1.2).set_fill(opacity=0.4),
            run_time=1
        )

        # Multi-touch activation
        self.play(Create(fingers), run_time=0.8)
        self.play(
            fingers.animate.scale(1.3).set_color(YELLOW),
            phone_screen.animate.set_fill(color=GOLD, opacity=0.4),
            run_time=1
        )
        self.play(
            fingers.animate.scale(1/1.3).set_color(RED),
            phone_screen.animate.set_fill(color=WHITE, opacity=0.2),
            run_time=1
        )

        # Final layout wait
        self.wait(2)
        
        # Cleanup / Conclusion of Scene 2
        self.play(
            FadeOut(phone),
            FadeOut(sqlite),
            FadeOut(nfc),
            FadeOut(touch_feat),
            FadeOut(fingers),
            run_time=1.5
        )