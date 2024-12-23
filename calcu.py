from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window

# شاشة الترحيب
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        welcome_label = Label(
            text="Welcome to the first experiences\nMy Instagram account is g.m0h1",
            font_size=32,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle"
        )
        layout.add_widget(welcome_label)
        self.add_widget(layout)

# شاشة تسجيل الدخول
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # إدخال اسم المستخدم
        self.username_input = TextInput(
            hint_text="Enter Username",
            font_size=24,
            size_hint=(1, 0.2),
            multiline=False
        )
        layout.add_widget(self.username_input)

        # إدخال كلمة المرور
        self.password_input = TextInput(
            hint_text="Enter Password",
            font_size=24,
            size_hint=(1, 0.2),
            password=True,
            multiline=False
        )
        layout.add_widget(self.password_input)

        # زر تسجيل الدخول
        self.login_button = Button(
            text="Login",
            font_size=24,
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.login_button.bind(on_press=self.validate_login)
        layout.add_widget(self.login_button)

        self.add_widget(layout)

    def validate_login(self, instance):
        # قائمة الحسابات المقبولة
        accounts = {
            "g.m0h1": "nour_houda",
            "asala_31": "asala_asala",
            "ilyas_001": "9ar9ora"
        }

        username = self.username_input.text
        password = self.password_input.text

        # التحقق من صحة المدخلات
        if accounts.get(username) == password:
            self.manager.current = "welcome_screen"
            self.manager.get_screen("welcome_screen").set_username(username)
        else:
            self.username_input.text = ''
            self.password_input.text = ''
            self.username_input.hint_text = "Invalid Username or Password"
            self.password_input.hint_text = "Invalid Username or Password"

# شاشة الترحيب بعد تسجيل الدخول
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.welcome_label = Label(
            text="Welcome, User!",
            font_size=32,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle"
        )
        layout.add_widget(self.welcome_label)

        # زر للدخول إلى الآلة الحاسبة
        self.start_button = Button(
            text="Go to Calculator",
            font_size=24,
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.start_button.bind(on_press=self.go_to_calculator)
        layout.add_widget(self.start_button)

        self.add_widget(layout)

    def set_username(self, username):
        self.welcome_label.text = f"Welcome, {username}!"

    def go_to_calculator(self, instance):
        self.manager.current = "calculator_screen"

# شاشة الآلة الحاسبة
class CalculatorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.operand = ""  # لتخزين العملية الحسابية
        self.dark_mode = True  # الوضع الافتراضي هو الوضع الداكن

        # تخطيط عمودي
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        # زر التبديل بين الوضعين
        self.switch_button = Button(
            text="Switch to Light Mode" if self.dark_mode else "Switch to Dark Mode",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=20
        )
        self.switch_button.bind(on_press=self.toggle_mode)
        layout.add_widget(self.switch_button)

        # مربع النص لعرض النتائج
        self.result_input = TextInput(
            text='',
            readonly=True,
            font_size=96,  # تكبير حجم النص
            halign='right',  # محاذاة النص إلى اليمين
            background_color=(0.1, 0.2, 0.3, 1),  # اللون الداكن الافتراضي
            foreground_color=(1, 1, 1, 1),  # النص أبيض في الوضع الداكن
            size_hint=(1, 0.3),  # تخصيص الحجم
            pos_hint={'top': 1},  # جعل النتيجة في الأعلى
            allow_copy=False,  # منع النسخ
            password=False,  # تعطيل اللصق
        )
        layout.add_widget(self.result_input)

        # إعداد الأزرار
        buttons = [
            ['7', '8', '9', '÷'],
            ['4', '5', '6', '×'],
            ['1', '2', '3', '-'],
            ['C', '0', '=', '+']
        ]

        # إضافة الأزرار للتخطيط
        for row in buttons:
            h_layout = BoxLayout(spacing=10, size_hint=(1, 0.2))  # ديناميكية ارتفاع الحاوية
            for label in row:
                button = Button(
                    text=label,
                    font_size=36,  # زيادة حجم النص
                    background_normal='',  # إزالة التصميم الافتراضي
                    background_color=self.get_button_color(label),  # ألوان حديثة
                    color=(1, 1, 1, 1),  # لون النص
                    size_hint=(1, 1),
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            layout.add_widget(h_layout)

        self.add_widget(layout)

        # تحديث السمة (التبديل بين الوضع الفاتح والداكن)
        self.update_theme()

    def update_theme(self):
        """تحديث الألوان بناءً على الوضع (فاتح أو داكن)"""
        if self.dark_mode:
            self.bg_color = (0.1, 0.2, 0.3, 1)  # خلفية داكنة
            self.fg_color = (1, 1, 1, 1)  # نص أبيض
            self.switch_button.background_color = (0.2, 0.6, 0.8, 1)  # لون الزر بالوضع الداكن
        else:
            self.bg_color = (1, 1, 1, 1)  # خلفية فاتحة
            self.fg_color = (0, 0, 0, 1)  # نص أسود
            self.switch_button.background_color = (0.8, 0.8, 0.8, 1)  # لون الزر بالوضع الفاتح

        self.result_input.background_color = self.bg_color
        self.result_input.foreground_color = self.fg_color

    def toggle_mode(self, instance):
        """تبديل الوضع بين الفاتح والداكن"""
        self.dark_mode = not self.dark_mode
        self.update_theme()
        self.switch_button.text = "Switch to Dark Mode" if self.dark_mode else "Switch to Light Mode"

    def get_button_color(self, label):
        """إرجاع لون زر بناءً على النص"""
        if label in ['C', '=', '÷', '×']:
            return (0.8, 0.1, 0.1, 1)  # أزرار حمراء
        elif label in ['+', '-', '*']:
            return (0.2, 0.6, 0.8, 1)  # أزرار زرقاء
        else:
            return (0.2, 0.8, 0.2, 1)  # أزرار خضراء

    def on_button_press(self, instance):
        text = instance.text

        # استبدال العلامات
        if text == '÷':
            text = '/'
        elif text == '×':
            text = '*'

        if text == 'C':
            self.operand = ''
        elif text == '=':
            try:
                self.operand = str(eval(self.operand))
            except Exception:
                self.operand = 'Error'
        else:
            self.operand += text

        self.result_input.text = self.operand


class CalculatorApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # شاشة الترحيب
        self.splash_screen = SplashScreen(name="splash")
        self.screen_manager.add_widget(self.splash_screen)

        # شاشة تسجيل الدخول
        self.login_screen = LoginScreen(name="login")
        self.screen_manager.add_widget(self.login_screen)

        # شاشة الترحيب بعد تسجيل الدخول
        self.welcome_screen = WelcomeScreen(name="welcome_screen")
        self.screen_manager.add_widget(self.welcome_screen)

        # شاشة الآلة الحاسبة
        self.calculator_screen = CalculatorScreen(name="calculator_screen")
        self.screen_manager.add_widget(self.calculator_screen)

        # الانتقال بعد 3 ثوانٍ من شاشة الترحيب إلى شاشة تسجيل الدخول
        Clock.schedule_once(self.switch_to_login, 3)

        return self.screen_manager

    def switch_to_login(self, dt):
        self.screen_manager.current = "login"


# تشغيل التطبيق
if __name__ == '__main__':
    CalculatorApp().run()