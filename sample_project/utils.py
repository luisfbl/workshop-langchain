"""Utilitários diversos."""

import os
import json


def read_json(filepath):
    # Lê arquivo JSON (sem docstring e sem type hints!)
    with open(filepath) as f:
        return json.load(f)


def write_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def list_files(directory):
    return os.listdir(directory)
