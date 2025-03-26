import flet as ft
from UI.view import View
from UI.controller import Controller

def main(page: ft.Page):
    v = View(page)
    c = Controller(v)
    v.setController(c)
    v.loadInterface()

ft.app(target = main)