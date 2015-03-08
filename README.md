#PFO Tools

A website with useful tools for Pathfinder Online

Currently consists of a django site with a single application: pfodb.

##pfodb

Provides a read-only JSON REST API for accessing game data.

Currently provides crafting/refining recipe information at '/pfodb/api'.

###Implementation

pfodb.models implements a collection of django Models representing various components of PFO. Certain Models are
tagged with a decorator that will include them in the API. The decorator contains the appropriate fields and their
associated serializers to use to provide the desired data. The metadata from these Models is collected and turned into
a tree derived from class inheritance and representing the API hierarchy. The tree is then processed to create a django
URLconf with nested paths & namespaces and the accompanying view functions to display the data as JSON.
