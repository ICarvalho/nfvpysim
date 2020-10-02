"""
This module contains all the information related to the current release of the
library including descriptions, version number, authors and contact
information.
"""
# author information.
# Used by __init__, doc and setup
author = 'Igor Furtado Carvalho'
author_email = 'igfuca@gmail.com'
maintainer = author
maintainer_email = author_email

# version information
# Used by __init__, doc and setup
__version__ = '0.1.0'

# License information
# Used by __init__, doc and setup
license_short = 'GNU GPLv2'
license_long = 'GNU GPLv2 license'

description_short = 'A scalable simulator for evaluating the performance of ' \
                    'in-network caches in Information Centric Networking (ICN)'

description_long = """Icarus is a Python-based discrete-event simulator for
evaluating the performance of networks of caches like Information
Centric Networks (ICN).
Icarus is not bound to any specific ICN architecture. Its design allows users to
implement and evaluate new caching policies or caching and routing strategy
with few lines of code.
"""

# URL

url = 'https://github.com/ICarvalho/TESE'
download_url = url