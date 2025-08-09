"""
Gunicorn configuration for production deployment
"""

import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
backlog = 2048

# Worker processes
workers = 1  # For free tier, keep it low
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 120
keepalive = 5
graceful_timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "book-recommender-api"

# Preload application
preload_app = True

# Restart workers
max_worker_memory = 300 * 1024 * 1024  # 300MB per worker (free tier limit)

def when_ready(server):
    server.log.info("🚀 Book Recommender API server is ready. Accepting connections.")

def worker_exit(server, worker):
    server.log.info(f"👋 Worker {worker.pid} exited.")

def on_starting(server):
    server.log.info("🏁 Starting Book Recommender API server...")

def on_reload(server):
    server.log.info("🔄 Reloading Book Recommender API server...")