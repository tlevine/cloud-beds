import cloud_beds.cli as cli

import nose.tools as n

def test_get_generator():
    n.assert_true(hasattr(cli.get_generator(), '__next__'))
