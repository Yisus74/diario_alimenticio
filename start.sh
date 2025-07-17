#!/bin/bash

echo "🌱 DIARIO DE ALIMENTACIÓN CONSCIENTE"
echo "==================================="
echo

# Verificar Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python no encontrado. Instala Python desde https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python encontrado: $($PYTHON_CMD --version)"
echo

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        echo "❌ pip no encontrado. Instala pip"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

echo "Instalando dependencias..."
$PIP_CMD install -r requirements.txt

echo
echo "Inicializando aplicación..."
$PYTHON_CMD run.py