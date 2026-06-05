import psutil
import datetime

class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        # Wenn Werte fehlen, messe sie jetzt
        self.cpu = cpu if cpu is not None else psutil.cpu_percent(interval=1)
        self.ram_total = ram_total if ram_total else psutil.virtual_memory().total
        self.ram_used = ram_used if ram_used else psutil.virtual_memory().used
        self.timestamp = timestamp if timestamp else datetime.datetime.now()