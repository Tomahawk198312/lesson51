import time
from datetime import datetime

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.metrics_history = []
        if HAS_PSUTIL:
            self.process = psutil.Process()
        else:
            self.process = None
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 75.0,
            'thread_count': 50
        }

    def get_metrics(self):
        if not HAS_PSUTIL:
            return {
                'timestamp': datetime.now(),
                'cpu_percent': 0.0,
                'memory_percent': 0.0,
                'thread_count': 0,
                'uptime': time.time() - self.start_time
            }
        metrics = {
            'timestamp': datetime.now(),
            'cpu_percent': self.process.cpu_percent(),
            'memory_percent': self.process.memory_percent(),
            'thread_count': len(self.process.threads()),
            'uptime': time.time() - self.start_time
        }
        self.metrics_history.append(metrics)
        if len(self.metrics_history) > 1000:
            self.metrics_history.pop(0)
        return metrics

    def check_health(self):
        metrics = self.get_metrics()
        if 'error' in metrics:
            return {'status': 'error', 'error': metrics['error']}
        status = {'status': 'healthy', 'warnings': []}
        if metrics['cpu_percent'] > self.thresholds['cpu_percent']:
            status['warnings'].append(f"High CPU: {metrics['cpu_percent']}%")
            status['status'] = 'warning'
        if metrics['memory_percent'] > self.thresholds['memory_percent']:
            status['warnings'].append(f"High memory: {metrics['memory_percent']}%")
            status['status'] = 'warning'
        if metrics['thread_count'] > self.thresholds['thread_count']:
            status['warnings'].append(f"High threads: {metrics['thread_count']}")
            status['status'] = 'warning'
        return status

    def log_metrics(self, logger):
        metrics = self.get_metrics()
        health = self.check_health()
        if 'error' not in metrics:
            logger.info(f"CPU: {metrics['cpu_percent']:.1f}%, Mem: {metrics['memory_percent']:.1f}%, Threads: {metrics['thread_count']}")
        if health['status'] == 'warning':
            for w in health['warnings']:
                logger.warning(f"Performance warning: {w}")