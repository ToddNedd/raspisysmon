import psutil
from subprocess import PIPE, Popen
import json

class SysInfo:
    def __init__(self, logger):
        self.logger = logger
        self.cpu_usage_percent = 0
        self.cpu_times_user = 0
        self.cpu_times_system = 0
        self.cpu_times_idle = 0
        self.cpu_freq_current = 0
        self.cpu_freq_min = 0
        self.cpu_freq_max = 0
        self.cpu_temp = 0
        self.mem_total = 0
        self.mem_available = 0
        self.mem_used = 0
        self.mem_free = 0
        self.mem_percent_used = 0
        self.disk_total = 0
        self.disk_used = 0
        self.disk_free = 0
        self.disk_percent_used = 0

    def __iter__(self):
        yield from {
            "cpu_usage_percent" : self.cpu_usage_percent,
            "cpu_times_user" : self.cpu_times_user,
            "cpu_times_system" : self.cpu_times_system,
            "cpu_times_idle": self.cpu_times_idle,
            "cpu_freq_current": self.cpu_freq_current,
            "cpu_freq_min": self.cpu_freq_min,
            "cpu_freq_max": self.cpu_freq_max,
            "cpu_temp": self.cpu_temp,
            "mem_total": self.mem_total,
            "mem_available": self.mem_available,
            "mem_used": self.mem_used,
            "mem_free": self.mem_free,
            "mem_percent_used": self.mem_percent_used,
            "disk_total": self.disk_total,
            "disk_used": self.disk_used,
            "disk_free": self.disk_free,
            "disk_percent_used": self.disk_percent_used
        }.items()

    def to_json(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def get_cpu_temperature(self):
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        output, _error = process.communicate()
        self.logger.info(f"vcgencmd: {output}")
        #return float(output[output.index('=') + 1:output.rindex("'")])
        retVal = float(output.split('=')[-1].strip().rstrip("'C"))
        self.logger.info(f"vcgencmd float: {retVal}")
        return retVal

    def update(self, withCpuTemp=True):
        self.cpu_usage_percent = psutil.cpu_percent(interval=1)
        cpu_times = psutil.cpu_times_percent(interval=1)
        self.cpu_times_user = cpu_times.user
        self.cpu_times_system = cpu_times.system
        self.cpu_times_idle = cpu_times.idle

        cpu_freq = psutil.cpu_freq()
        self.cpu_freq_current = cpu_freq.current
        self.cpu_freq_min = cpu_freq.min
        self.cpu_freq_max = cpu_freq.max

        if withCpuTemp == True:
            self.logger.info("try call vcgencmd")
            self.cpu_temp = self.get_cpu_temperature()

        mem = psutil.virtual_memory()
        self.mem_total = mem.total
        self.mem_available = mem.available
        self.mem_used = mem.used
        self.mem_free = mem.free
        self.mem_percent_used = mem.percent

        disk = psutil.disk_usage('/')
        self.disk_total = disk.total
        self.disk_used = disk.used
        self.disk_free = disk.free
        self.disk_percent_used = disk.percent
        

    