#!/bin/bash

# Server-Hostname
SERVER="www2"

# Benutzername für die SSH-Verbindung
USERNAME="flask-reader"

# Führe den Befehl "deploy" auf dem Remote-Server aus
ssh $USERNAME@$SERVER 'cd pdf_form; git pull'
ssh $USERNAME@$SERVER 'sudo ./deploy-pdfform.sh > /dev/null'

