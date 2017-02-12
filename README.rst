Component Generator
===================

Attempt to reduce the bolierplate code that is written almost everyday.

Usage
-----

.. code:: sh

    usage: Use "component_generator --help" for more information

    Reduce the boiler plate when writting components.

    positional arguments:
      component_names       A list of comopents to stub out

    optional arguments:
      -h, --help            show this help message and exit
      -t [str [str ...]], --storage-types [str [str ...]]
                            A list of storage types to generate. A `pure_memory`
                            storage type will always be generated.
      -a [json], --logic-arguments [json]
                            Extend logic and client methods by adding arguments to
                            default methods '{"package": {"create_{0}": ["foo"]}'
                            or add new methods in the same way '{"package":
                            {"spam": ["eggs"]}}'
      -k [json], --logic-kwarguments [json]
                            Extend logic and client methods by adding keyword
                            arguments to default methods '{"package":
                            {"create_{0}": {"foo": null}}' or add new methods in
                            the same way '{"package": {"spam": {"eggs": false}}}'
      -r [json], --storage-arguments [json]
                            Extend storage methods by adding arguments to default
                            methods: '{"package": {"create_{0}": ["foo"]}' or add
                            new methods in the same way: '{"package": {"spam":
                            ["eggs"]}}'
      -w [json], --storage-kwarguments [json]
                            Extend logic and client methods by adding keyword
                            arguments to default methods '{"package":
                            {"create_{0}": {"foo": null}}' or add new methods in
                            the same way '{"package": {"spam": {"eggs": false}}}'
      -p [PATH], --path [PATH]
                            Where to generate the component.
      -c [CONFIG], --config [CONFIG]
                            Path the a configuration to use.
      -v, --verbose         Set logging level to DEBUG

TODO
----

- [X] Add argparse / optparse 'ing
- [X] Allow multiple componets to be generated simultaneously
- [] Allow defining class level attributres
- [X] Generate component in current directory, not library directory
- [] Implement injection setup
- [] Implement test interfaces
- [] Expand README to show examples and a more robust explanation of what
  problem(s) this library solves
- [] Make it publishable to PyPI
