import time
from datetime import datetime

class Analytics:
    def __init__(self, cache):
        self.cache = cache
        self.start_time = time.time()
        self.model_usage = {}
        self.session_data = []
        self._load_historical_data()

    def _load_historical_data(self):
        history = self.cache.get_analytics_history()
        for ts, model, msg_len, resp_time, tokens in history:
            self.model_usage.setdefault(model, {'count': 0, 'tokens': 0})
            self.model_usage[model]['count'] += 1
            self.model_usage[model]['tokens'] += tokens
            self.session_data.append({
                'timestamp': datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f'),
                'model': model,
                'message_length': msg_len,
                'response_time': resp_time,
                'tokens_used': tokens
            })

    def track_message(self, model, message_length, response_time, tokens_used):
        timestamp = datetime.now()
        self.cache.save_analytics(timestamp, model, message_length, response_time, tokens_used)
        self.model_usage.setdefault(model, {'count': 0, 'tokens': 0})
        self.model_usage[model]['count'] += 1
        self.model_usage[model]['tokens'] += tokens_used
        self.session_data.append({
            'timestamp': timestamp,
            'model': model,
            'message_length': message_length,
            'response_time': response_time,
            'tokens_used': tokens_used
        })

    def get_statistics(self):
        total_time = time.time() - self.start_time
        total_tokens = sum(m['tokens'] for m in self.model_usage.values())
        total_messages = sum(m['count'] for m in self.model_usage.values())
        return {
            'total_messages': total_messages,
            'total_tokens': total_tokens,
            'session_duration': total_time,
            'messages_per_minute': (total_messages * 60) / total_time if total_time > 0 else 0,
            'tokens_per_message': total_tokens / total_messages if total_messages > 0 else 0,
            'model_usage': self.model_usage
        }

    def export_data(self):
        return self.session_data

    def clear_data(self):
        self.model_usage.clear()
        self.session_data.clear()