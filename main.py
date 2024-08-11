import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Escolar")
        self.geometry("800x600")
        
        self.current_view = None
        self.show_login()

    def show_login(self):
        self.switch_view(LoginView)

    def show_dashboard(self):
        self.switch_view(DashboardView)

    def show_attendance(self):
        self.switch_view(AttendanceView)

    def show_tracking(self):
        self.switch_view(TrackingView)

    def show_help(self):
        self.switch_view(HelpView)

    def switch_view(self, view_class):
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = view_class(self)
        self.current_view.pack(fill=tk.BOTH, expand=True)

class LoginView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()
        
        tk.Label(self, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        
        tk.Button(self, text="Login", command=self.login).pack()

    def login(self):
        # Aquí iría la lógica de autenticación
        self.master.show_dashboard()

class BaseView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_menu()

    def create_menu(self):
        menu_frame = tk.Frame(self)
        menu_frame.pack(side=tk.TOP, fill=tk.X)
        
        buttons = [
            ("Dashboard", self.master.show_dashboard),
            ("Asistencia", self.master.show_attendance),
            ("Seguimiento", self.master.show_tracking),
            ("Ayuda", self.master.show_help)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command).pack(side=tk.LEFT)

class DashboardView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.create_graphs()

    def create_graphs(self):
        graphs_frame = tk.Frame(self)
        graphs_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Gráfico de asistencia (pie chart)
        fig1, ax1 = plt.subplots()
        data = [30, 10, 5]
        labels = ['Presente', 'Tardanza', 'Falta']
        ax1.pie(data, labels=labels, autopct='%1.1f%%')
        ax1.set_title("Asistencia del día")
        
        canvas1 = FigureCanvasTkAgg(fig1, master=graphs_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Gráfico de notas promedio (bar chart)
        fig2, ax2 = plt.subplots()
        subjects = ['Mat', 'Len', 'Hist', 'Cien']
        grades = [15, 17, 14, 16]
        ax2.bar(subjects, grades)
        ax2.set_title("Notas promedio")
        ax2.set_ylim(0, 20)
        
        canvas2 = FigureCanvasTkAgg(fig2, master=graphs_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # DateEntry para seleccionar fecha
        date_frame = tk.Frame(self)
        date_frame.pack(side=tk.TOP, fill=tk.X)
        self.date_entry = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=10)

class AttendanceView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.create_attendance_table()

    def create_attendance_table(self):
        columns = ("N°", "Nombre", "Asistió", "Tardanza", "Faltó")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        data = [
            (1, "Juan", True, False, False),
            (2, "Maria", False, True, False),
            (3, "Luis", False, True, False),
            (4, "Ana", False, True, False),
            (5, "Carlos", False, False, True),
        ]
        
        for item in data:
            values = (item[0], item[1], "✓" if item[2] else "", "✓" if item[3] else "", "✓" if item[4] else "")
            tree.insert("", tk.END, values=values)
        
        tree.pack(fill=tk.BOTH, expand=True)

class TrackingView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.create_tracking_view()

    def create_tracking_view(self):
        # Buscador de alumnos
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="Buscar alumno:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        tk.Button(search_frame, text="Buscar", command=self.search_student).pack(side=tk.LEFT)

        # Información del alumno
        self.info_frame = tk.Frame(self)
        self.info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def search_student(self):
        # Simular búsqueda de alumno
        student_name = self.search_entry.get()
        self.display_student_info(student_name)

    def display_student_info(self, name):
        # Limpiar frame de información
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Mostrar información del alumno
        tk.Label(self.info_frame, text=f"Alumno: {name}").pack()
        
        # Comportamiento
        tk.Label(self.info_frame, text="Comportamiento hoy:").pack()
        ttk.Combobox(self.info_frame, values=["Excelente", "Bueno", "Regular", "Malo"]).pack()

        # Cursos inscritos
        tk.Label(self.info_frame, text="Cursos inscritos:").pack()
        tk.Listbox(self.info_frame).pack(fill=tk.X)

        # Otras estadísticas
        stats = {
            "Promedio de notas": "15.5",
            "% de asistencias": "85%",
            "N° de puesto": "5",
            "N° de faltas": "3"
        }
        for key, value in stats.items():
            tk.Label(self.info_frame, text=f"{key}: {value}").pack()

class HelpView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.create_faq()

    def create_faq(self):
        tk.Label(self, text="Preguntas Frecuentes", font=("Arial", 16, "bold")).pack(pady=10)

        faqs = [
            ("¿Cómo registro la asistencia?", "Ve a la sección 'Asistencia' y marca la casilla correspondiente."),
            ("¿Cómo busco a un alumno?", "En la sección 'Seguimiento', usa el buscador en la parte superior."),
            ("¿Cómo cambio mi contraseña?", "Ve a 'Configuración' y selecciona 'Cambiar contraseña'."),
        ]

        for question, answer in faqs:
            frame = tk.Frame(self)
            frame.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(frame, text=question, font=("Arial", 12, "bold")).pack(anchor=tk.W)
            tk.Label(frame, text=answer, wraplength=700).pack(anchor=tk.W)

if __name__ == "__main__":
    app = App()
    app.mainloop()