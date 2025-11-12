#!/bin/sh

echo "Bootstrapping database..."
python bootstrap_db.py

echo "Starting Flask app..."
python app.py
