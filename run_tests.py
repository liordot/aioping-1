import argparse
import io
import os
import platform
import smtplib
import subprocess
import sys
import time
import unittest

def output_system_info(log):
    pipe = subprocess.PIPE
    p = subprocess.Popen(['git', 'log', '--oneline', '-n 1'], stdout=pipe,
                         stderr=pipe)
    stdout, stderr = p.communicate()
    p.kill()

    print(item for item in [
        '%s\n' % time.asctime(),
        'os.name: %s\n' % os.name,
        'platform.system: %s\n' % platform.system(),
        'platform.release: %s\n' % platform.release(),
        'commit: %s\n' % stdout.decode().split()[0],
        'Python version (via sys.version): %s\n\n' % sys.version
    ])


def run_tests(log, v=2):
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromName('builder')
    runner = unittest.TextTestRunner(stream=log, buffer=True, verbosity=v)
    runner.run(tests)


log = io.StringIO()
output_system_info(log)
run_tests(log)

# UNCOMMENT TO ADD TO tests.log
# with open('logs/tests.log', 'a+') as test_log:
#     l.test_logger.info('Appending test results to tests log.')
#     test_log.writelines([line for line in log.getvalue()])

print(log.getvalue())
