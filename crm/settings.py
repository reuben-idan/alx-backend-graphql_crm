# Django Crontab Configuration for CRM App

# Add django_crontab to INSTALLED_APPS
INSTALLED_APPS = [
    'django_crontab',
]

# Configure CRONJOBS for heartbeat logging and low stock updates
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
] 