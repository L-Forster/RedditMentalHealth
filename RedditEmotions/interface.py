from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
import facade
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.garden.graph import BarPlot, MeshLinePlot, Graph

KV = '''
MDScreen:

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
    

        Label:
            id: output_text
            font_style: "H5"
            bold: True
            text: ""   
            halign: "center"
            valign: "center"
            
    MDTextField:
        id: raw_data
        hint_text: "Enter raw data"
        helper_text_mode: "on_error"
        helper_text: "Input is required"
        size_hint_x: .9
        pos_hint: {"center_x":.5, "center_y": .5}
        on_text_validate: app.on_enter_raw()

        
    FloatLayout:

        CustomBarChart:  # Use the CustomBarChart widget
            id: bar_chart
            size_hint: (0.6,0.4)



    MDTextField:
        id: username
        hint_text: "Enter Reddit username"
        helper_text_mode: "on_error"
        helper_text: "Input is required"
        pos_hint: {"center_x": .275, "center_y": .9}
        size_hint_x: .5
        on_text_validate: app.on_enter_reddit()


        
    MDLabel:
        id: output_text
        font_style: "H5"
        bold: True
        text: ""   
        halign: "center"
        valign: "center"
        pos_hint: {"center_y": .1}
        size_hint_x: 1
        theme_text_color: "Error"


    MDSwitch:
        id: switch_depression
        pos_hint: {'center_x': 0.05, 'center_y': .8}
        on_active: app.update_disorder("depression")
    MDLabel:
        id: depression_text
        text: "- Depression"
        pos_hint: {'center_x': .6, 'center_y': .8}
    MDLabel:
        id: depression_acc
        text: str(app.getAccuracy("depression"))
        pos_hint: {'center_x': .9, 'center_y': .8}
        
    MDSwitch:
        id: switch_adh
        pos_hint: {'center_x': 0.05, 'center_y': .75}
        on_active: app.update_disorder("adhd")
    MDLabel:
        id: adhd_text
        text: "- ADHD"
        pos_hint: {'center_x': .6, 'center_y': .75}
    MDLabel:
        id: adhd_acc
        text: str(app.getAccuracy("adhd"))
        pos_hint: {'center_x': .9, 'center_y': .75}


    MDSwitch:
        id: switch_bipolar
        pos_hint: {'center_x': 0.05, 'center_y': .7}
        on_active: app.update_disorder("bipolar")
    MDLabel:
        id: bipolar_text
        text: "- Bipolar"
        pos_hint: {'center_x': .6, 'center_y': .7}
    MDLabel:
        id: bipolar_acc
        text: str(app.getAccuracy("bipolar"))
        pos_hint: {'center_x': .9, 'center_y': .7}
        
    MDSwitch:
        id: switch_narcissism
        pos_hint: {'center_x': 0.05, 'center_y': .65}
        on_active: app.update_disorder("narcissism")
    MDLabel:
        id: narcissism_text
        text: "- Narcissism"
        pos_hint: {'center_x': .6, 'center_y': .65}
    MDLabel:
        id: narcissism_acc
        text: str(app.getAccuracy("narcissism"))
        pos_hint: {'center_x': .9, 'center_y': .65}        
        
    MDSwitch:
        id: switch_antisocial
        pos_hint: {'center_x': 0.05, 'center_y': .6}
        on_active: app.update_disorder("aspd")
    MDLabel:
        id: aspd_text
        text: "- ASPD"
        pos_hint: {'center_x': .6, 'center_y': .6}
    MDLabel:
        id: aspd_acc
        text: str(app.getAccuracy("aspd"))
        pos_hint: {'center_x': .9, 'center_y': .6}              
        
    MDSwitch:
        id: switch_schizophrenia
        pos_hint: {'center_x': 0.05, 'center_y': .55}
        on_active: app.update_disorder("schizophrenia")
        
    MDLabel:
        id: schizophrenia_text
        text: "- Schizophrenia"
        pos_hint: {'center_x': .6, 'center_y': .55}
    MDLabel:
        id: schizophrenia_acc
        text: str(app.getAccuracy("schizophrenia"))
        pos_hint: {'center_x': .9, 'center_y': .55}          

    MDFillRoundFlatButton:
        text: "Update Selected Disorders"
        # md_bg_color: "red"
        pos_hint: {'center_x': .87, 'center_y': .05}
        on_press: app.update_data()
            
            
'''

class CustomBarChart(FloatLayout):
    def __init__(self, labels=[], values= [], **kwargs):
        super(CustomBarChart, self).__init__(**kwargs)
        self.labels = labels
        self.values = values
        self.create_chart()

    def create_chart(self):
        graph = Graph(xlabel='Disorder', ylabel='Probability', x_ticks_minor=5, x_ticks_major=25,y_ticks_major=1, y_grid_label=True,
                      x_grid_label=True, padding=5, x_grid=True, y_grid=True, ymax=1)

        num_bars = len(self.labels)
        if num_bars > 0:
            bar_spacing = 10
            bar_width = (90 - (num_bars - 1) * bar_spacing) / num_bars
            x_pos = bar_spacing

            for label, value in zip(self.labels, self.values):
                if value > 0.6:
                    plot = MeshLinePlot(color=(255,0,0,1))

                else:
                    plot = MeshLinePlot(color=(0,128,128,1))
                plot.points = [(x_pos, 0), (x_pos, value), (x_pos + bar_width, value), (x_pos + bar_width, 0)]
                x_pos += bar_width + bar_spacing
                graph.add_plot(plot)
                label_text = Label(text=label, pos=((x_pos - bar_width)*5 - 270, int(-30 + value*200)), size=(bar_width, 30), halign='left')
                self.add_widget(label_text)
                # graph.x_grid_label =
            self.add_widget(graph)

class Redditor(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        self.subreddits = []
        self.chart_container = BoxLayout(orientation="vertical")

        probs = []
    def getAccuracy(self, disorder):
        f = open("accuracy_values/"+disorder+" acc.txt", "r")
        acc_val = (f.read())
        acc_val=  round(float(acc_val),4)

        f.close()
        return "Accuracy: " + str(acc_val)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.screen.ids.username.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        return self.screen
    def update_disorder(self, name):
        if name in self.subreddits:
            self.subreddits.remove(name)
        else:
            self.subreddits.append(name)


    def update_data(self):
        for sub in self.subreddits:
            facade.main(sub, "", "update")
            tempId = str(sub) + "_acc"
            label = self.root.ids[tempId]
            label.text = self.getAccuracy(sub)
    def set_error_message(self, instance_textfield):
        if instance_textfield.text == "":
            self.screen.ids.username.error = True

    def on_enter_raw(self):
        probs = []
        data = self.screen.ids.raw_data.text
        for subreddit in self.subreddits:
            probs.append((subreddit,facade.main(subreddit, data, "raw")))

        probs = sorted(probs, key=lambda x: x[0])
        self.root.ids.bar_chart.clear_widgets()
        l = [item[0] for item in probs]
        v = [item[1] for item in probs]
        custom_bar_chart = CustomBarChart(labels=l,values=v)
        self.root.ids.bar_chart.add_widget(custom_bar_chart)
        # self.screen.ids.output_text.text = str(probs)


    def on_enter_reddit(self):
        username = self.screen.ids.username.text
        if username == "":
            return -1
        # get data from username
        prob = -1
        probs = []
        for subreddit in self.subreddits:
            prob = facade.main(subreddit, username, "user")
            if prob <= 1 and prob >= 0:
                probs.append((subreddit,prob))
            else:
                self.screen.ids.output_text.text = "User has not posted!"
        probs = sorted(probs, key=lambda x: x[0])
        self.root.ids.bar_chart.clear_widgets()
        l = [item[0] for item in probs]
        v = [item[1] for item in probs]
        custom_bar_chart = CustomBarChart(labels=l,values=v)
        self.root.ids.bar_chart.add_widget(custom_bar_chart)
        self.root.ids.output_text.text = ""


Redditor().run()
