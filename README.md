Uliweb-Admin
==============

What's it?
-----------

It's a admin app designed for Uliweb. The features lists below:

* Model can be configured to using Admin
* Display a data grid of each configured Model
* You can Create, Edit, Display, Delete records

Requirements
-------------

* uliweb
* plugs

Demo requires:

* par (from Blog Demo)
* SQLAlchemy
* database driver (default is sqlite shipped in python 2.6 & 2.7 already)

Demo
------

There is a demo project shipped in project, you can use it to test.

1. Install all required packages, just do:

    ```
    cd demo
    uliweb install
    ```

    It should install all you need.

2. Create tables to database. If you want to use mysql you coult set it in `local_settings.ini`.

    ```
    uliweb syncdb
    ```

3. Create an superuser user in order to use uliweb-admin app, just do:

    ```
    uliweb createsuperuser
    ```
    
4. Start develop server to test:

    ```
    uliweb runserver
    ```

    Then enter `http://localhost:8000/admin` you'll see the admin interface.

License
---------

This project release under BSD license.