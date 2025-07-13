# CRM Celery Setup Guide

This guide provides step-by-step instructions for setting up Celery with Redis for the CRM application.

## Prerequisites

- Python 3.8+
- Django 4.2.11
- Redis server

## Installation Steps

### 1. Install Redis

#### On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### On macOS:

```bash
brew install redis
brew services start redis
```

#### On Windows:

Download Redis from https://redis.io/download and follow the installation instructions.

### 2. Install Python Dependencies

All required packages are already included in `requirements.txt`:

- celery==5.3.4
- django-celery-beat==2.5.0
- redis==5.0.1
- gql==3.4.1

Install them using:

```bash
pip install -r requirements.txt
```

### 3. Run Django Migrations

```bash
python manage.py migrate
```

This will create the necessary database tables for django-celery-beat.

### 4. Start Celery Worker

In a new terminal window, start the Celery worker:

```bash
celery -A crm worker -l info
```

The worker will start and listen for tasks.

### 5. Start Celery Beat

In another terminal window, start Celery Beat (the scheduler):

```bash
celery -A crm beat -l info
```

This will schedule and trigger the CRM report generation task.

### 6. Verify Setup

#### Check Redis Connection:

```bash
redis-cli ping
```

Should return `PONG`

#### Test Celery Task:

```bash
python manage.py shell
```

Then in the shell:

```python
from crm.tasks import generate_crm_report
result = generate_crm_report.delay()
print(result.get())
```

#### Check Logs:

Monitor the log file for reports:

- **Linux/macOS**: `/tmp/crm_report_log.txt`
- **Windows**: `C:/temp/crm_report_log.txt`

## Scheduled Tasks

### CRM Report Generation

- **Schedule**: Every Monday at 6:00 AM
- **Task**: `crm.tasks.generate_crm_report`
- **Output**: Logs to `crm_report_log.txt`

The report includes:

- Total number of customers
- Total number of orders
- Total revenue (sum of order amounts)

## Troubleshooting

### Common Issues

1. **Redis Connection Error**:

   - Ensure Redis is running: `redis-cli ping`
   - Check Redis configuration in `crm/celery.py`

2. **Django Settings Not Found**:

   - Ensure `DJANGO_SETTINGS_MODULE` is set correctly
   - Run from the project root directory

3. **GraphQL Connection Error**:

   - Ensure Django server is running on `http://localhost:8000`
   - Check GraphQL endpoint accessibility

4. **Task Not Executing**:
   - Verify Celery worker is running
   - Check Celery Beat scheduler is active
   - Review task logs for errors

### Log Files

- **Celery Worker Logs**: Console output from worker process
- **Celery Beat Logs**: Console output from beat process
- **CRM Report Logs**: `/tmp/crm_report_log.txt` (Linux/macOS) or `C:/temp/crm_report_log.txt` (Windows)

## Production Deployment

For production environments:

1. **Use a process manager** (Supervisor, systemd) to manage Celery processes
2. **Configure Redis persistence** for data durability
3. **Set up monitoring** for Celery tasks and Redis
4. **Use environment variables** for sensitive configuration
5. **Implement proper logging** and error handling

## Example Log Output

```
2025-07-14 06:00:00 - Report: 25 customers, 150 orders, $12500.00 revenue
2025-07-21 06:00:00 - Report: 28 customers, 165 orders, $13875.50 revenue
```
