import flet as ft
from flet import (
    AppBar, Column, Container, ElevatedButton, Icon, IconButton, 
    NavigationRail, NavigationRailDestination, OutlinedButton, 
    Page, Row, SnackBar, Tab, Tabs, Text, TextField, 
    Colors, Icons, padding, border, border_radius,
    alignment, MainAxisAlignment, CrossAxisAlignment, TextButton,
    VerticalDivider, Card, Image, ProgressBar, Checkbox, Divider,
    ListView, GridView, Dropdown, dropdown, Control, margin
)
import json
import requests
from datetime import datetime

# Configuração da API Django
API_URL = "http://localhost:8000/api"  # Ajuste para o endereço do seu backend Django

# Classe para gerenciar autenticação
class AuthManager:
    def __init__(self):
        self.token = None
        self.user_data = None
        self.is_volunteer = False
    
    def login(self, username, password):
        # Simulação de login - em produção, conectaria ao Django
        if username and password:
            self.token = "sample_token"
            self.user_data = {
                "id": 1,
                "name": "João Silva",
                "email": "joao@exemplo.com",
                "phone": "(11) 98765-4321",
                "is_volunteer": self.is_volunteer
            }
            return True
        return False
    
    def logout(self):
        self.token = None
        self.user_data = None
        return True
    
    def is_authenticated(self):
        return self.token is not None

# Classe principal da aplicação
class MusicLearningApp(Control):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.auth_manager = AuthManager()
        self.current_view = "home"
        self.selected_course = None
        self.selected_instrument = None
        
        # Dados simulados - em produção, viriam da API Django
        self.load_mock_data()
        
    def _get_control_name(self):
        return "music-learning-app"
    
    def load_mock_data(self):
        # Artigos
        self.articles = [
            {
                "id": 1,
                "title": "Como Escolher Seu Primeiro Instrumento",
                "excerpt": "Um guia completo para ajudar iniciantes a escolher o instrumento ideal para começar sua jornada musical.",
                "category": "Guia",
                "date": "15 de Maio, 2023",
                "image": "https://via.placeholder.com/300x200?text=Instrumento"
            },
            {
                "id": 2,
                "title": "Fundamentos da Teoria Musical",
                "excerpt": "Entenda os conceitos básicos da teoria musical que todo músico iniciante deve conhecer.",
                "category": "Teoria",
                "date": "10 de Maio, 2023",
                "image": "https://via.placeholder.com/300x200?text=Teoria"
            },
            {
                "id": 3,
                "title": "Técnicas de Prática Eficiente",
                "excerpt": "Aprenda como maximizar seu tempo de prática e evoluir mais rapidamente em seu instrumento.",
                "category": "Prática",
                "date": "5 de Maio, 2023",
                "image": "https://via.placeholder.com/300x200?text=Prática"
            }
        ]
        
        # Instrumentos
        self.instruments = [
            {
                "id": 1,
                "name": "Violão Clássico",
                "description": "Violão para iniciantes em bom estado.",
                "source": "ONGs",
                "image": "https://via.placeholder.com/300x200?text=Violão"
            },
            {
                "id": 2,
                "name": "Piano Digital",
                "description": "Piano digital com 88 teclas, ideal para estudantes.",
                "source": "Professores",
                "image": "https://via.placeholder.com/300x200?text=Piano"
            },
            {
                "id": 3,
                "name": "Flauta Doce",
                "description": "Flauta doce soprano, perfeita para iniciantes.",
                "source": "ONGs",
                "image": "https://via.placeholder.com/300x200?text=Flauta"
            }
        ]
        
        # Cursos
        self.courses = [
            {
                "id": 1,
                "title": "Violão para Iniciantes",
                "description": "Aprenda os acordes básicos e comece a tocar suas músicas favoritas.",
                "level": "Iniciante",
                "duration": "4 semanas",
                "students": 1245,
                "progress": 65,
                "enrolled": True,
                "image": "https://via.placeholder.com/300x200?text=Violão",
                "lessons": [
                    {
                        "id": 1,
                        "title": "Introdução ao Violão",
                        "duration": "15 min",
                        "description": "Conheça as partes do violão e aprenda a postura correta para tocar.",
                        "completed": True,
                        "video_url": "https://example.com/video1"
                    },
                    {
                        "id": 2,
                        "title": "Primeiros Acordes",
                        "duration": "20 min",
                        "description": "Aprenda os acordes básicos: Dó (C), Sol (G) e Ré (D).",
                        "completed": True,
                        "video_url": "https://example.com/video2"
                    },
                    {
                        "id": 3,
                        "title": "Ritmos Básicos",
                        "duration": "25 min",
                        "description": "Pratique ritmos simples para acompanhar músicas populares.",
                        "completed": False,
                        "video_url": "https://example.com/video3"
                    },
                    {
                        "id": 4,
                        "title": "Sua Primeira Música",
                        "duration": "30 min",
                        "description": "Aprenda a tocar uma música completa usando os acordes e ritmos aprendidos.",
                        "completed": False,
                        "video_url": "https://example.com/video4"
                    }
                ]
            },
            {
                "id": 2,
                "title": "Fundamentos do Piano",
                "description": "Domine as técnicas básicas do piano e leitura de partituras.",
                "level": "Iniciante",
                "duration": "6 semanas",
                "students": 890,
                "progress": 30,
                "enrolled": True,
                "image": "https://via.placeholder.com/300x200?text=Piano",
                "lessons": []
            },
            {
                "id": 3,
                "title": "Introdução à Bateria",
                "description": "Aprenda ritmos básicos e técnicas de coordenação na bateria.",
                "level": "Iniciante",
                "duration": "5 semanas",
                "students": 723,
                "progress": 0,
                "enrolled": False,
                "image": "https://via.placeholder.com/300x200?text=Bateria",
                "lessons": []
            }
        ]
        
        # Horários disponíveis
        self.available_slots = [
            {"id": 1, "time": "09:00 - 10:00", "date": "18/05/2023", "instrument_id": 1, "booked": False},
            {"id": 2, "time": "10:00 - 11:00", "date": "18/05/2023", "instrument_id": 1, "booked": False},
            {"id": 3, "time": "14:00 - 15:00", "date": "18/05/2023", "instrument_id": 2, "booked": True},
            {"id": 4, "time": "15:00 - 16:00", "date": "19/05/2023", "instrument_id": 3, "booked": False}
        ]
        
        # Instrumentos gerenciados por voluntários
        self.volunteer_instruments = [
            {
                "id": 1,
                "name": "Violão Clássico",
                "description": "Violão para iniciantes em bom estado.",
                "available": True,
                "bookings": 5
            },
            {
                "id": 2,
                "name": "Flauta Doce",
                "description": "Flauta doce soprano, perfeita para iniciantes.",
                "available": True,
                "bookings": 2
            },
            {
                "id": 3,
                "name": "Ukulele",
                "description": "Ukulele soprano em ótimo estado.",
                "available": False,
                "bookings": 0
            }
        ]
    
    def build(self):
        # Barra de navegação
        self.nav_rail = NavigationRail(
            selected_index=0,
            label_type="all",
            min_width=100,
            min_extended_width=200,
            destinations=[
                NavigationRailDestination(
                    icon=Icons.HOME_OUTLINED,
                    selected_icon=Icons.HOME,
                    label="Início"
                ),
                NavigationRailDestination(
                    icon=Icons.ARTICLE_OUTLINED,
                    selected_icon=Icons.ARTICLE,
                    label="Artigos"
                ),
                NavigationRailDestination(
                    icon=Icons.MUSIC_NOTE_OUTLINED,
                    selected_icon=Icons.MUSIC_NOTE,
                    label="Instrumentos"
                ),
                NavigationRailDestination(
                    icon=Icons.SCHOOL_OUTLINED,
                    selected_icon=Icons.SCHOOL,
                    label="Cursos"
                ),
                NavigationRailDestination(
                    icon=Icons.PERSON_OUTLINED,
                    selected_icon=Icons.PERSON,
                    label="Perfil"
                ),
            ],
            on_change=self.nav_change
        )
        
        # Conteúdo principal
        self.content_area = Container(
            content=self.get_home_view(),
            expand=True,
            padding=20
        )
        
        # Layout principal
        return Row([
            self.nav_rail,
            VerticalDivider(width=1),
            self.content_area
        ], expand=True)
    
    def nav_change(self, e):
        index = e.control.selected_index
        views = ["home", "articles", "instruments", "courses", "profile"]
        self.current_view = views[index]
        
        # Verificar autenticação para views protegidas
        if self.current_view in ["instruments", "courses", "profile"] and not self.auth_manager.is_authenticated():
            self.content_area.content = self.get_login_view()
        else:
            # Atualizar conteúdo baseado na navegação
            if self.current_view == "home":
                self.content_area.content = self.get_home_view()
            elif self.current_view == "articles":
                self.content_area.content = self.get_articles_view()
            elif self.current_view == "instruments":
                self.content_area.content = self.get_instruments_view()
            elif self.current_view == "courses":
                self.content_area.content = self.get_courses_view()
            elif self.current_view == "profile":
                self.content_area.content = self.get_profile_view()
        
        self.content_area.update()
    
    # Views da aplicação
    def get_home_view(self):
        # Seção de destaque
        hero_section = Container(
            content=Column([
                Text("Aprenda Música no Seu Ritmo", size=40, weight="bold"),
                Text(
                    "Descubra o mundo dos instrumentos musicais e desenvolva suas habilidades com nossos cursos e recursos.",
                    size=16,
                    color=Colors.BLACK54
                ),
                Container(height=20),
                ElevatedButton(
                    "Explorar Cursos",
                    icon=Icons.ARROW_FORWARD,
                    on_click=lambda _: self.navigate_to("courses")
                )
            ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER),
            padding=padding.all(40),
            alignment=alignment.center,
            bgcolor=Colors.GREEN_50,
            border_radius=10,
            margin=margin.only(bottom=20)
        )
        
        # Cards de acesso rápido
        quick_access_cards = Row([
            Card(
                content=Container(
                    content=Column([
                        Icon(Icons.ARTICLE, size=50, color=Colors.GREEN),
                        Text("Artigos Públicos", weight="bold"),
                        Text("Confira nossos artigos sobre teoria musical e técnicas de aprendizado.", 
                             size=12, color=Colors.BLACK54),
                        TextButton("Ver Artigos →", on_click=lambda _: self.navigate_to("articles"))
                    ], spacing=10, alignment=MainAxisAlignment.CENTER),
                    padding=15,
                    alignment=alignment.center
                ),
                elevation=3,
                width=200
            ),
            Card(
                content=Container(
                    content=Column([
                        Icon(Icons.MUSIC_NOTE, size=50, color=Colors.AMBER),
                        Text("Instrumentos Musicais", weight="bold"),
                        Text("Explore nossa coleção de instrumentos disponíveis para aprendizado.", 
                             size=12, color=Colors.BLACK54),
                        TextButton("Ver Instrumentos →", on_click=lambda _: self.navigate_to("instruments"))
                    ], spacing=10, alignment=MainAxisAlignment.CENTER),
                    padding=15,
                    alignment=alignment.center
                ),
                elevation=3,
                width=200
            ),
            Card(
                content=Container(
                    content=Column([
                        Icon(Icons.SCHOOL, size=50, color=Colors.PINK),
                        Text("Mini-Cursos", weight="bold"),
                        Text("Comece a aprender com nossos mini-cursos para iniciantes.", 
                             size=12, color=Colors.BLACK54),
                        TextButton("Ver Cursos →", on_click=lambda _: self.navigate_to("courses"))
                    ], spacing=10, alignment=MainAxisAlignment.CENTER),
                    padding=15,
                    alignment=alignment.center
                ),
                elevation=3,
                width=200
            )
        ], alignment=MainAxisAlignment.CENTER, spacing=20)
        
        # Atualizações recentes
        updates = Column([
            Container(
                content=Row([
                    Container(
                        content=Icon(Icons.MUSIC_NOTE, color=Colors.GREEN),
                        bgcolor=Colors.GREEN_50,
                        padding=10,
                        border_radius=5
                    ),
                    Column([
                        Text("Novo Curso de Violão", weight="bold"),
                        Text("Aprenda os fundamentos do violão em nosso novo curso para iniciantes.", 
                             size=12, color=Colors.BLACK54),
                        Text("2 dias atrás", size=10, color=Colors.BLACK38)
                    ], spacing=5)
                ], spacing=10),
                padding=10,
                border=border.all(1, Colors.BLACK12),
                border_radius=5,
                margin=margin.only(bottom=10)
            ),
            Container(
                content=Row([
                    Container(
                        content=Icon(Icons.ARTICLE, color=Colors.GREEN),
                        bgcolor=Colors.GREEN_50,
                        padding=10,
                        border_radius=5
                    ),
                    Column([
                        Text("Artigo: Teoria Musical Básica", weight="bold"),
                        Text("Um guia completo sobre os fundamentos da teoria musical para iniciantes.", 
                             size=12, color=Colors.BLACK54),
                        Text("5 dias atrás", size=10, color=Colors.BLACK38)
                    ], spacing=5)
                ], spacing=10),
                padding=10,
                border=border.all(1, Colors.BLACK12),
                border_radius=5,
                margin=margin.only(bottom=10)
            )
        ])
        
        recent_updates_section = Container(
            content=Column([
                Text("Atualizações Recentes", size=20, weight="bold"),
                Container(height=10),
                updates
            ]),
            padding=20,
            bgcolor=Colors.WHITE,
            border_radius=10,
            border=border.all(1, Colors.BLACK12)
        )
        
        return Column([
            hero_section,
            Container(
                content=quick_access_cards,
                alignment=alignment.center,
                margin=margin.only(bottom=20)
            ),
            recent_updates_section
        ], scroll=True)
    
    def get_articles_view(self):
        articles_grid = GridView(
            expand=1,
            max_extent=350,
            spacing=10,
            run_spacing=10,
            padding=20,
            child_aspect_ratio=0.8
        )
        
        for article in self.articles:
            articles_grid.controls.append(
                Card(
                    content=Container(
                        content=Column([
                            Image(
                                src=article["image"],
                                width=350,
                                height=200,
                                fit="cover"
                            ),
                            Container(
                                content=Column([
                                    Container(
                                        content=Text(article["category"], size=12),
                                        bgcolor=Colors.GREEN_50,
                                        padding=padding.only(left=8, right=8, top=4, bottom=4),
                                        border_radius=15
                                    ),
                                    Text(article["title"], size=18, weight="bold"),
                                    Text(article["excerpt"], size=14, color=Colors.BLACK54),
                                    Row([
                                        Text(article["date"], size=12, color=Colors.BLACK38),
                                        TextButton("Ler mais →")
                                    ], alignment=MainAxisAlignment.SPACE_BETWEEN)
                                ], spacing=10),
                                padding=15
                            )
                        ])
                    ),
                    elevation=2
                )
            )
        
        return Column([
            Text("Artigos sobre Música", size=30, weight="bold"),
            Text("Explore nossos artigos sobre teoria musical, técnicas e história.", 
                 size=16, color=Colors.BLACK54),
            Container(height=20),
            articles_grid
        ], scroll=True)
    
    def get_instruments_view(self):
        if not self.auth_manager.is_authenticated():
            return self.get_login_view("Acesso Restrito", 
                                      "Faça login para acessar informações sobre instrumentos disponíveis e gerenciar seus instrumentos.")
        
        instruments_grid = GridView(
            expand=1,
            max_extent=300,
            spacing=10,
            run_spacing=10,
            padding=20,
            child_aspect_ratio=0.7
        )
        
        for instrument in self.instruments:
            instruments_grid.controls.append(
                Card(
                    content=Container(
                        content=Column([
                            Image(
                                src=instrument["image"],
                                width=300,
                                height=200,
                                fit="cover"
                            ),
                            Container(
                                content=Column([
                                    Row([
                                        Container(
                                            content=Text(instrument["source"], size=12),
                                            bgcolor=Colors.GREEN_50,
                                            padding=padding.only(left=8, right=8, top=4, bottom=4),
                                            border_radius=15
                                        )
                                    ], alignment=MainAxisAlignment.END),
                                    Text(instrument["name"], size=18, weight="bold"),
                                    Text(instrument["description"], size=14, color=Colors.BLACK54),
                                    ElevatedButton(
                                        "Agendar Instrumento",
                                        icon=Icons.CALENDAR_TODAY,
                                        on_click=lambda _, inst=instrument: self.show_instrument_booking(inst)
                                    )
                                ], spacing=10),
                                padding=15
                            )
                        ])
                    ),
                    elevation=2
                )
            )
        
        # Seção de agendamento
        booking_section = Container(
            content=Column([
                Text("Horários Disponíveis", size=20, weight="bold"),
                Container(height=10),
                ListView(
                    controls=[
                        Container(
                            content=Row([
                                Text(f"{slot['date']} | {slot['time']}", size=14),
                                Text(next((i["name"] for i in self.instruments if i["id"] == slot["instrument_id"]), ""), size=14),
                                Container(
                                    content=Text("Reservado" if slot["booked"] else "Disponível", size=12),
                                    bgcolor=Colors.RED_50 if slot["booked"] else Colors.GREEN_50,
                                    padding=padding.only(left=8, right=8, top=4, bottom=4),
                                    border_radius=15
                                ),
                                ElevatedButton(
                                    "Reservar",
                                    disabled=slot["booked"],
                                    on_click=lambda _, s=slot: self.book_slot(s)
                                )
                            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                            padding=10,
                            border=border.all(1, Colors.BLACK12),
                            border_radius=5,
                            margin=margin.only(bottom=5)
                        ) for slot in self.available_slots
                    ],
                    height=200,
                    spacing=2
                )
            ]),
            padding=20,
            bgcolor=Colors.WHITE,
            border_radius=10,
            border=border.all(1, Colors.BLACK12),
            margin=margin.only(top=20)
        )
        
        return Column([
            Text("Instrumentos Musicais", size=30, weight="bold"),
            Text("Explore e agende instrumentos disponíveis para prática.", 
                 size=16, color=Colors.BLACK54),
            Container(height=20),
            instruments_grid,
            booking_section
        ], scroll=True)
    
    def get_courses_view(self):
        if not self.auth_manager.is_authenticated():
            return self.get_login_view("Acesso Restrito", 
                                      "Faça login para acessar nossos mini-cursos e começar sua jornada musical.")
        
        # Se um curso específico foi selecionado, mostrar detalhes do curso
        if self.selected_course:
            return self.get_course_detail_view(self.selected_course)
        
        courses_grid = GridView(
            expand=1,
            max_extent=350,
            spacing=10,
            run_spacing=10,
            padding=20,
            child_aspect_ratio=0.7
        )
        
        for course in self.courses:
            courses_grid.controls.append(
                Card(
                    content=Container(
                        content=Column([
                            Image(
                                src=course["image"],
                                width=350,
                                height=200,
                                fit="cover"
                            ),
                            Container(
                                content=Column([
                                    Row([
                                        Container(
                                            content=Text(course["level"], size=12),
                                            bgcolor=Colors.GREEN_50,
                                            padding=padding.only(left=8, right=8, top=4, bottom=4),
                                            border_radius=15
                                        )
                                    ], alignment=MainAxisAlignment.END),
                                    Text(course["title"], size=18, weight="bold"),
                                    Text(course["description"], size=14, color=Colors.BLACK54),
                                    Row([
                                        Text(f"Duração: {course['duration']}", size=12, color=Colors.BLACK54),
                                        Text(f"{course['students']} alunos", size=12, color=Colors.BLACK54)
                                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                                    Container(height=10),
                                    Column([
                                        Row([
                                            Text("Progresso:", size=12),
                                            Text(f"{course['progress']}%", size=12)
                                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                                        ProgressBar(value=course["progress"] / 100)
                                    ]) if course["enrolled"] else Container(),
                                    Container(height=10),
                                    ElevatedButton(
                                        "Continuar Curso" if course["enrolled"] else "Iniciar Curso",
                                        on_click=lambda _, c=course: self.show_course_detail(c)
                                    )
                                ], spacing=10),
                                padding=15
                            )
                        ])
                    ),
                    elevation=2
                )
            )
        
        return Column([
            Text("Mini-Cursos para Iniciantes", size=30, weight="bold"),
            Text("Aprenda a tocar instrumentos musicais com nossos cursos estruturados.", 
                 size=16, color=Colors.BLACK54),
            Container(height=20),
            courses_grid
        ], scroll=True)
    
    def get_course_detail_view(self, course):
        lessons_list = ListView(
            spacing=10,
            padding=20
        )
        
        for i, lesson in enumerate(course["lessons"]):
            lessons_list.controls.append(
                Container(
                    content=Column([
                        Row([
                            Container(
                                content=Text(str(i+1), color=Colors.WHITE, text_align="center"),
                                width=30,
                                height=30,
                                bgcolor=Colors.GREEN if lesson["completed"] else Colors.GREY,
                                border_radius=15,
                                alignment=alignment.center
                            ),
                            Column([
                                Text(lesson["title"], weight="bold"),
                                Text(f"Duração: {lesson['duration']}", size=12, color=Colors.BLACK54)
                            ]),
                            Icon(
                                Icons.CHECK_CIRCLE if lesson["completed"] else Icons.PLAY_CIRCLE_OUTLINE,
                                color=Colors.GREEN if lesson["completed"] else Colors.GREY
                            )
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        Container(
                            content=Column([
                                Text(lesson["description"], size=14),
                                Container(height=10),
                                Row([
                                    OutlinedButton(
                                        "Assistir Vídeo",
                                        icon=Icons.PLAY_ARROW
                                    ),
                                    ElevatedButton(
                                        "Marcar como Concluído",
                                        disabled=lesson["completed"],
                                        on_click=lambda _, l=lesson: self.complete_lesson(l)
                                    )
                                ], alignment=MainAxisAlignment.END)
                            ]),
                            padding=padding.only(left=30, top=10),
                            visible=True  # Em uma implementação real, isso seria controlado por um estado de expansão
                        )
                    ]),
                    padding=10,
                    border=border.all(1, Colors.BLACK12),
                    border_radius=10
                )
            )
        
        return Column([
            IconButton(
                icon=Icons.ARROW_BACK,
                on_click=lambda _: self.back_to_courses()
            ),
            Container(
                content=Row([
                    Image(
                        src=course["image"],
                        width=150,
                        height=150,
                        fit="cover",
                        border_radius=10
                    ),
                    Column([
                        Text(course["title"], size=24, weight="bold"),
                        Text(course["description"], size=16, color=Colors.BLACK54),
                        Container(height=10),
                        Row([
                            Container(
                                content=Text(course["level"], size=12),
                                bgcolor=Colors.GREEN_50,
                                padding=padding.only(left=8, right=8, top=4, bottom=4),
                                border_radius=15
                            ),
                            Text(f"Duração: {course['duration']}", size=14)
                        ], spacing=10)
                    ], spacing=5, expand=True)
                ], spacing=20),
                padding=20
            ),
            Container(
                content=Column([
                    Text("Seu Progresso", weight="bold"),
                    Container(height=5),
                    Row([
                        Text(f"{course['progress']}% Concluído", size=14),
                        Text(f"{len([l for l in course['lessons'] if l['completed']])}/{len(course['lessons'])} lições", size=14)
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Container(height=5),
                    ProgressBar(value=course["progress"] / 100)
                ]),
                padding=20,
                bgcolor=Colors.GREEN_50,
                border_radius=10
            ),
            Container(height=20),
            Text("Lições do Curso", size=20, weight="bold"),
            lessons_list
        ], scroll=True)
    
    def get_profile_view(self):
        if not self.auth_manager.is_authenticated():
            return self.get_login_view()
        
        # Verificar se é perfil de voluntário ou estudante
        if self.auth_manager.is_volunteer:
            return self.get_volunteer_profile_view()
        
        # Perfil de estudante
        user = self.auth_manager.user_data
        
        # Cursos matriculados
        enrolled_courses = ListView(
            spacing=10,
            height=200
        )
        
        for course in [c for c in self.courses if c["enrolled"]]:
            enrolled_courses.controls.append(
                Container(
                    content=Row([
                        Image(
                            src=course["image"],
                            width=80,
                            height=80,
                            fit="cover",
                            border_radius=5
                        ),
                        Column([
                            Text(course["title"], weight="bold"),
                            Text(f"Progresso: {course['progress']}%", size=14),
                            ProgressBar(value=course["progress"] / 100, width=200)
                        ], spacing=5, expand=True),
                        IconButton(
                            icon=Icons.ARROW_FORWARD,
                            on_click=lambda _, c=course: self.show_course_detail(c)
                        )
                    ], spacing=10),
                    padding=10,
                    border=border.all(1, Colors.BLACK12),
                    border_radius=10
                )
            )
        
        # Agendamentos
        bookings = ListView(
            spacing=10,
            height=200
        )
        
        for slot in [s for s in self.available_slots if s["booked"]]:
            instrument = next((i for i in self.instruments if i["id"] == slot["instrument_id"]), None)
            if instrument:
                bookings.controls.append(
                    Container(
                        content=Row([
                            Column([
                                Text(f"Data: {slot['date']}", size=14),
                                Text(f"Horário: {slot['time']}", size=14),
                                Text(f"Instrumento: {instrument['name']}", size=14)
                            ], spacing=5, expand=True),
                            OutlinedButton(
                                "Cancelar",
                                icon=Icons.CANCEL,
                                on_click=lambda _, s=slot: self.cancel_booking(s)
                            )
                        ]),
                        padding=10,
                        border=border.all(1, Colors.BLACK12),
                        border_radius=10
                    )
                )
        
        return Column([
            Text("Perfil do Usuário", size=30, weight="bold"),
            Container(height=20),
            
            # Informações pessoais
            Container(
                content=Column([
                    Text("Informações Pessoais", size=20, weight="bold"),
                    Container(height=10),
                    TextField(label="Nome Completo", value=user["name"]),
                    TextField(label="E-mail", value=user["email"]),
                    TextField(label="Celular", value=user["phone"]),
                    Container(height=10),
                    ElevatedButton(
                        "Atualizar Perfil",
                        icon=Icons.SAVE,
                        on_click=lambda _: self.update_profile()
                    )
                ]),
                padding=20,
                bgcolor=Colors.WHITE,
                border_radius=10,
                border=border.all(1, Colors.BLACK12)
            ),
            
            Container(height=20),
            
            # Cursos matriculados
            Container(
                content=Column([
                    Text("Meus Cursos", size=20, weight="bold"),
                    Container(height=10),
                    enrolled_courses if enrolled_courses.controls else Text("Você não está matriculado em nenhum curso.", color=Colors.BLACK54)
                ]),
                padding=20,
                bgcolor=Colors.WHITE,
                border_radius=10,
                border=border.all(1, Colors.BLACK12)
            ),
            
            Container(height=20),
            
            # Agendamentos
            Container(
                content=Column([
                    Text("Meus Agendamentos", size=20, weight="bold"),
                    Container(height=10),
                    bookings if bookings.controls else Text("Você não tem agendamentos ativos.", color=Colors.BLACK54)
                ]),
                padding=20,
                bgcolor=Colors.WHITE,
                border_radius=10,
                border=border.all(1, Colors.BLACK12)
            )
        ], scroll=True)
    
    def get_volunteer_profile_view(self):
        # Perfil para ONGs e professores voluntários
        
        # Instrumentos gerenciados
        managed_instruments = ListView(
            spacing=10,
            height=200
        )
        
        for instrument in self.volunteer_instruments:
            managed_instruments.controls.append(
                Container(
                    content=Row([
                        Column([
                            Text(instrument["name"], weight="bold"),
                            Text(instrument["description"], size=14),
                            Row([
                                Container(
                                    content=Text("Disponível" if instrument["available"] else "Indisponível", size=12),
                                    bgcolor=Colors.GREEN_50 if instrument["available"] else Colors.RED_50,
                                    padding=padding.only(left=8, right=8, top=4, bottom=4),
                                    border_radius=15
                                ),
                                Text(f"{instrument['bookings']} agendamentos", size=12)
                            ], spacing=10)
                        ], spacing=5, expand=True),
                        OutlinedButton(
                            "Editar",
                            icon=Icons.EDIT,
                            on_click=lambda _, i=instrument: self.edit_instrument(i)
                        )
                    ]),
                    padding=10,
                    border=border.all(1, Colors.BLACK12),
                    border_radius=10
                )
            )
        
        # Agenda
        schedule = ListView(
            spacing=10,
            height=200
        )
        
        for slot in self.available_slots:
            instrument = next((i for i in self.instruments if i["id"] == slot["instrument_id"]), None)
            if instrument:
                schedule.controls.append(
                    Container(
                        content=Row([
                            Column([
                                Text(f"Data: {slot['date']}", size=14),
                                Text(f"Horário: {slot['time']}", size=14),
                                Text(f"Instrumento: {instrument['name']}", size=14),
                                Container(
                                    content=Text("Reservado" if slot["booked"] else "Disponível", size=12),
                                    bgcolor=Colors.RED_50 if slot["booked"] else Colors.GREEN_50,
                                    padding=padding.only(left=8, right=8, top=4, bottom=4),
                                    border_radius=15
                                )
                            ], spacing=5, expand=True),
                            OutlinedButton(
                                "Remover",
                                icon=Icons.DELETE,
                                on_click=lambda _, s=slot: self.remove_slot(s)
                            )
                        ]),
                        padding=10,
                        border=border.all(1, Colors.BLACK12),
                        border_radius=10
                    )
                )
        
        return Column([
            Text("Perfil de Voluntário", size=30, weight="bold"),
            Container(height=20),
            
            # Informações pessoais
            Container(
                content=Column([
                    Text("Informações da Organização", size=20, weight="bold"),
                    Container(height=10),
                    TextField(label="Nome da Organização", value="ONG Música para Todos"),
                    TextField(label="E-mail", value="contato@musicaparatodos.org"),
                    TextField(label="Telefone", value="(11) 3456-7890"),
                    Container(height=10),
                    ElevatedButton(
                        "Atualizar Perfil",
                        icon=Icons.SAVE,
                        on_click=lambda _: self.update_profile()
                    )
                ]),
                padding=20,
                bgcolor=Colors.WHITE,
                border_radius=10,
                border=border.all(1, Colors.BLACK12)
            ),
            
            Container(height=20),
            
            # Instrumentos gerenciados
            Container(
                content=Column([
                    Row([
                        Text("Instrumentos Gerenciados", size=20, weight="bold"),
                        ElevatedButton(
                            "Adicionar Instrumento",
                            icon=Icons.ADD,
                            on_click=lambda _: self.add_instrument()
                        )
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Container(height=10),
                    managed_instruments
                ]),
                padding=20,
                bgcolor=Colors.WHITE,
                border_radius=10,
                border=border.all(1, Colors.BLACK12)
            ),
            
            Container(height=20),
            
            # Agenda
            Container(
                content=Column([
                    Row([
                        Text("Gerenciar Agenda", size=20, weight="bold"),
                        ElevatedButton(
                            "Adicionar Horário",
                            icon=Icons.ADD,
                            on_click=lambda _: self.add_time_slot()
                        )
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Container(height=10),
                    schedule
                ]),
                padding=20,
                bgcolor=Colors.WHITE,
                border_radius=10,
                border=border.all(1, Colors.BLACK12)
            )
        ], scroll=True)
    
    def get_login_view(self, title="Acesso Restrito", message="Faça login para acessar esta área."):
        return Container(
            content=Column([
                Icon(Icons.LOCK, size=50, color=Colors.AMBER),
                Text(title, size=24, weight="bold"),
                Text(message, size=16, color=Colors.BLACK54, text_align="center"),
                Container(height=20),
                TextField(
                    label="Usuário",
                    border=border.all(1, Colors.BLACK26),
                    border_radius=5,
                    prefix_icon=Icons.PERSON
                ),
                TextField(
                    label="Senha",
                    password=True,
                    border=border.all(1, Colors.BLACK26),
                    border_radius=5,
                    prefix_icon=Icons.LOCK
                ),
                Container(height=10),
                Row([
                    Checkbox(label="Entrar como ONG/Professor Voluntário", value=False, on_change=self.toggle_volunteer_login),
                ], alignment=MainAxisAlignment.CENTER),
                Container(height=10),
                ElevatedButton(
                    "Entrar",
                    icon=Icons.LOGIN,
                    on_click=lambda _: self.perform_login()
                ),
                TextButton("Criar uma conta")
            ], alignment=MainAxisAlignment.CENTER, horizontal_alignment=CrossAxisAlignment.CENTER),
            alignment=alignment.center,
            padding=40,
            bgcolor=Colors.WHITE,
            width=400,
            border_radius=10,
            border=border.all(1, Colors.BLACK12)
        )
    
    # Métodos de ação
    def navigate_to(self, view):
        views = ["home", "articles", "instruments", "courses", "profile"]
        index = views.index(view)
        self.nav_rail.selected_index = index
        self.nav_change(ft.ControlEvent(self.nav_rail, "change", None, None))
    
    def toggle_volunteer_login(self, e):
        self.auth_manager.is_volunteer = e.control.value
    
    def perform_login(self):
        # Simulação de login
        self.auth_manager.login("user", "password")
        
        # Redirecionar para a página atual
        if self.current_view == "home":
            self.content_area.content = self.get_home_view()
        elif self.current_view == "articles":
            self.content_area.content = self.get_articles_view()
        elif self.current_view == "instruments":
            self.content_area.content = self.get_instruments_view()
        elif self.current_view == "courses":
            self.content_area.content = self.get_courses_view()
        elif self.current_view == "profile":
            self.content_area.content = self.get_profile_view()
        
        self.content_area.update()
        
        # Mostrar mensagem de sucesso
        self.page.snack_bar = SnackBar(
            content=Text("Login realizado com sucesso!"),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def show_course_detail(self, course):
        self.selected_course = course
        self.content_area.content = self.get_course_detail_view(course)
        self.content_area.update()
    
    def back_to_courses(self):
        self.selected_course = None
        self.content_area.content = self.get_courses_view()
        self.content_area.update()
    
    def complete_lesson(self, lesson):
        lesson["completed"] = True
        
        # Atualizar progresso do curso
        if self.selected_course:
            total_lessons = len(self.selected_course["lessons"])
            completed_lessons = len([l for l in self.selected_course["lessons"] if l["completed"]])
            self.selected_course["progress"] = round((completed_lessons / total_lessons) * 100)
            
            # Atualizar na lista de cursos
            for course in self.courses:
                if course["id"] == self.selected_course["id"]:
                    course["progress"] = self.selected_course["progress"]
        
        # Atualizar a view
        self.content_area.content = self.get_course_detail_view(self.selected_course)
        self.content_area.update()
        
        # Mostrar mensagem de sucesso
        self.page.snack_bar = SnackBar(
            content=Text("Lição concluída com sucesso!"),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def show_instrument_booking(self, instrument):
        self.selected_instrument = instrument
        
        # Em uma implementação real, isso abriria um diálogo de agendamento
        self.page.snack_bar = SnackBar(
            content=Text(f"Agendamento para {instrument['name']} será implementado em breve."),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def book_slot(self, slot):
        slot["booked"] = True
        
        # Atualizar a view
        self.content_area.content = self.get_instruments_view()
        self.content_area.update()
        
        # Mostrar mensagem de sucesso
        self.page.snack_bar = SnackBar(
            content=Text("Horário reservado com sucesso!"),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def cancel_booking(self, slot):
        slot["booked"] = False
        
        # Atualizar a view
        self.content_area.content = self.get_profile_view()
        self.content_area.update()
        
        # Mostrar mensagem de sucesso
        self.page.snack_bar = SnackBar(
            content=Text("Reserva cancelada com sucesso!"),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def update_profile(self):
        # Em uma implementação real, isso enviaria os dados para o backend
        self.page.snack_bar = SnackBar(
            content=Text("Perfil atualizado com sucesso!"),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def add_instrument(self):
        # Em uma implementação real, isso abriria um diálogo para adicionar instrumento
        self.page.snack_bar = SnackBar(
            content=Text("Funcionalidade de adicionar instrumento será implementada em breve."),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def edit_instrument(self, instrument):
        # Em uma implementação real, isso abriria um diálogo para editar instrumento
        self.page.snack_bar = SnackBar(
            content=Text(f"Edição do instrumento {instrument['name']} será implementada em breve."),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def add_time_slot(self):
        # Em uma implementação real, isso abriria um diálogo para adicionar horário
        self.page.snack_bar = SnackBar(
            content=Text("Funcionalidade de adicionar horário será implementada em breve."),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def remove_slot(self, slot):
        # Em uma implementação real, isso removeria o horário
        self.available_slots.remove(slot)
        
        # Atualizar a view
        self.content_area.content = self.get_volunteer_profile_view()
        self.content_area.update()
        
        # Mostrar mensagem de sucesso
        self.page.snack_bar = SnackBar(
            content=Text("Horário removido com sucesso!"),
            action="OK"
        )
        self.page.snack_bar.open = True
        self.page.update()

def main(page: Page):
    page.title = "MusicaMaster - Aprenda Música"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    app = MusicLearningApp(page)
    page.add(app)
    page.update()

if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=8550,
        assets_dir="app/assets"
    )