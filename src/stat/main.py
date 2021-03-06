#!/usr/bin/env python
# -*- coding: utf-8-unix -*-
from __future__ import absolute_import, print_function, division, unicode_literals

import copy
import json
import sys

from anova import Anova
from chisquare import ChiSquare
from correlation import Correlation
from hypothesis_testing import ZTesting, DependentTTesting, IndependentTTesting
from sample import Sample


__author__ = "Benny Prijono <benny@stosia.com>"
__copyright__ = "Copyright (C)2017 PT. Stosia Teknologi Investasi"
__license__ = "GNU Affero AGPL (AGPL) version 3.0 or later"


if __name__ == "__main__":
    def usage():
        print("Usage:")
        print("  stat CMD [-i filename] [-o filename] [-csv filename]")
        print("")
        print("  CMD            -sample, -ztest, -dttest, -ittest, -anova, -corr, -chi")
        print("  -i filename    Read parameters from file")
        print("  -o filename    Write parameters to file")
        print("  -csv filename  Read data from this CSV file")

    class MyEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

    classes = {
        'sample': Sample,
        'dttest': DependentTTesting,
        'ittest': IndependentTTesting,
        'ztest': ZTesting,
        'anova': Anova,
        'corr': Correlation,
        'chi': ChiSquare,
        }

    session = input_file = output_file = csv_file = None
    cmds = ['-' + k for k in classes.keys()]
    args = ""
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in cmds:
            session = classes[arg[1:]]()
        elif arg in ["-h", "--help", "/?"]:
            usage()
            sys.exit(0)
        elif arg == "-i":
            i += 1
            input_file = sys.argv[i]
        elif arg == "-o":
            i += 1
            output_file = sys.argv[i]
        elif arg == '-csv':
            i += 1
            csv_file = sys.argv[i]
        else:
            args += " " + arg
        i += 1

    if not session and not input_file:
        sys.stderr.write("Error: -t or -z must be specified\n\n")
        usage()
        sys.exit(1)

    if input_file:
        if session:
            sys.stderr.write("Error: -i cannot be used with CMD\n")
            sys.exit(1)

        with open(input_file) as f:
            body = f.read()
            d = json.loads(body)

        class_name = d['class']
        for c in classes.itervalues():
            if class_name == c.__name__:
                session = c()
                break

        if not session:
            sys.stderr.write("Error: invalid class %s\n\n" % class_name)
            sys.exit(1)
        session.load_from_dict(d)
    else:
        session.input_wizard(csv_filename=csv_file)
        print("End of input wizard")
        print("")

    if output_file:
        with open(output_file, 'wt') as f:
            d = copy.copy(session.save_to_dict())
            d['class'] = session.__class__.__name__
            f.write(json.dumps(d, indent=4, cls=MyEncoder, sort_keys=True))

    session.print_report()

