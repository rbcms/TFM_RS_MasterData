#!/usr/bin/env python
""""
ojo!!! si da error de módulo, especificar la versión exacta de phyton.
En mi caso es la 3.6
Si no no encuentra el core.django.

"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
