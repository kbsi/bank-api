import logging
from app.services.mongo import get_log_collection


class MongoHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_collection = get_log_collection()
        log_collection.insert_one({
            "level": record.levelname,
            "message": log_entry,
            "timestamp": record.created,
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
            "pathname": record.pathname
        })
