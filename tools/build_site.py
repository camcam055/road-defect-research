#!/usr/bin/env python3
"""Rebuild shared navigation and interactive sections without changing report text."""
from layout import build_shell
from build_sections import build
if __name__ == "__main__":
    build_shell()
    build()
