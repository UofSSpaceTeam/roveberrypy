Adding to the documentation
---------------------------
This page outlines how to add your own stuff to the documentation page.

Documentation for the Roveberrypy project is done in sphinx, like many
python projects these days.
Sphinx takes files written in `reStructuredText`_ (rst), and generates
nice html pages from them, simmilar to how markdown works.
The big selling feature of Sphinx though, is its ability to extract
python `Docstrings`_ and insert them in your html pages, meaning that
once you have your basic page looking the way you want, sphinx will
keep the pretty html pages up to date with your documentation comments
in the source code its self.

For the rover processes that you make, just add standard python docstrings
to your classes, methods and functions. I have enabled the napoleon
extention for sphinx, so you use Google conventions for documenting
parameters, return types, etc like so::

    """ Constructor, called in main.py automatically, don't override this through inheritance.

        Args:
            uplink (multiprocessing.Queue): queue for outgoing messages
            downlink (multiprocessing.Queue): queue for incomming messages
    """

This will be turned into something like this:

.. automethod:: roverprocess.RoverProcess.RoverProcess.__init__
    :noindex:

The expected data type of parameters is given in parenthesis, and if you use a type
that is defined in the Roveberrypy software, sphinx will create a hyperlink to the
apporopriate documentation page.

To make sphinx actually see your module and generate an entry for it, open
the roverprocess.rst file and add something like this::

    roverprocess.MyProcess module
    ----------------------------------

    .. automodule:: roverprocess.MyProcess
        :members:
        :undoc-members:
        :show-inheritance:

If your module requires more sophisticated documentation on how to use it,
a new page can be made and linked to before your call to automodule.

Install sphinx on your machine and do a ``make html`` from the docs directory to build the docs.
open the generated index page from ``docs/build/html/index.html`` in a web browser to check that your
documentation looks correct.

When your feature branch is merged with the dev branch, ReadTheDocs will automatically build
the latest docs from the dev branch.

.. _Docstrings: https://www.python.org/dev/peps/pep-0257/
.. _reStructuredText: http://www.sphinx-doc.org/en/stable/rest.html
