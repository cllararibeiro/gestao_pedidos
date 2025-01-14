from gestao_pedidos import app
from flask import render_template, redirect, url_for, request


@app.route('/')
def index():
    return "Teste"