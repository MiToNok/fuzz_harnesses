"""
An issue was discovered in Django 5.0 before 5.0.8 and 4.2 before 4.2.15.
QuerySet.values() and values_list() methods on models with a JSONField are
subject to SQL injection in column aliases via a crafted JSON object key as a passed *arg
"""