# Django Crontab Configuration for CRM App

# Add django_crontab to INSTALLED_APPS
INSTALLED_APPS = [
    'django_crontab',
]

# Configure CRONJOBS for heartbeat logging
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
] 