Introduction
------------

This extension allows you resize your sphinx RTD site.

Usage
-----

`pip install sphinx-rtd-size`

.. code-block::
   :caption: conf.py

    import sphinx_rtd_size

    extensions = [
        ...
        'sphinx_rtd_size',
    ]
    
    sphinx_rtd_size_width = "90%"
