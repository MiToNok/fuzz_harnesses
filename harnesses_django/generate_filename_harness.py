""""
An issue was discovered in Django 5.0 before 5.0.7 and 4.2 before 4.2.14.
Derived classes of the django.core.files.storage.Storage base class,
when they override generate_filename() without replicating the file-path validations from the parent class,
potentially allow directory traversal via certain inputs during a save() call. (Built-in Storage sub-classes are unaffected.)
"""