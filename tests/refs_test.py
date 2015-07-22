"""Nose test."""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import zip
import subprocess, os, glob, shutil, re, sys


def test_demo():
    for name in glob.glob('tmp_diff*'):  # clean old diff files
        os.remove(name)

    # The test is a Bash script, record output and put to file
    failure, output = subprocess.getstatusoutput('export PYTHONPATH=; sh refs_demo.sh')
    if failure:
        print(output)
        raise OSError('test_demo: could not run the test script run refs_demo.sh!')
    # Line with 'Saving invalid papers to ...' contains the date,
    # strip that off
    output = re.sub(r'^Saving invalid papers to.+$', '', output,
                    flags=re.MULTILINE)
    with open('refs_demo.out', 'w') as f :
        f.write(output)

    # Strip off date and time in invalid_papers*.pub
    for filename in glob.glob('invalid_papers-*'):
        shutil.copy(filename, 'invalid_papers.pub')


    # Compare all files generated (incl. output from script)
    reference_data = 'reference_data'
    files = ['papers.pub', 'venues.list', 'refs_demo.sh',
             'refs_demo.out', 'invalid_papers.pub', 'present.html']
    for filename in files :
        ref_file = os.path.join(reference_data, filename)
#        ref_files = [os.path.join(reference_data, filename) for
#                 filename in files]
#    failure = pydiff(ref_files, files)
        failure = pydiff(ref_file, filename)
        success = not failure
        msg = """
New data in {} differs from reference data! Check out the files
tmp_diff*.txt (plain text comparison) or load tmp_diff*.html
into a browser for visual inspection of differences.
If differences are correct, run copy_new_reference_data.sh
to update the reference files.
""".format(filename)
        assert success, msg


def test_config_publish_import():
    """
    Override config data using local_config_publish_import/publish_config.py.
    The database and venues names are different and a capitalization
    typo is corrected.
    """
    for name in glob.glob('tmp_diff*'):  # clean old diff files
        os.remove(name)

    # Checking import publish_config does not work from here,
    # but works fine from publish

    # The test is a Bash script, record output and put to file.
    # Must set PYTHONPATH in OS subprocess (sys.path cannot be
    # changed in this script - that has no effect on the OS subprocess)
    failure, output = subprocess.getstatusoutput(
        'export PYTHONPATH=local_config_publish_import:$PYTHONPATH; sh refs_demo.sh')
    if failure:
        print(output)
        raise OSError('test_config_publish_import: could not run the test script run refs_demo.sh!')
    # Line with 'Saving invalid papers to ...' contains the date,
    # strip that off
    output = re.sub(r'^Saving invalid papers to.+$', '', output,
                    flags=re.MULTILINE)
    # User config...imported from... contains absolute path, strip off
    output = re.sub(r'^User configuration data imported from .+$', '', output,
                    flags=re.MULTILINE)
    f = open('refs_demo_with_local_config_publish_import.out', 'w')
    f.write(output)
    f.close()
    # Strip off date and time in invalid_papers*.pub
    for filename in glob.glob('invalid_papers-*'):
        shutil.copy(filename, 'invalid_papers.pub')

    # Compare all files generated (incl. output from script)
    reference_data = 'reference_data'
    files = ['publish_papers1.pub', 'publish_venues1.txt',
             'refs_demo.sh',
             'refs_demo_with_local_config_publish_import.out',
             'invalid_papers.pub',
             'present.html', 'present.bib']
    for filename in files :
        ref_file = os.path.join(reference_data, filename)

        failure = pydiff(ref_file, filename)
        success = not failure
        msg = """
New data in {} differs from reference data! Check out the files
tmp_diff*.txt (plain text comparison) or load tmp_diff*.html
into a browser for visual inspection of differences.
If differences are correct, run copy_new_reference_data.sh
to update the reference files.
""".format(filename)
        assert success, msg

def test_config_no_import():
    """
    Override config data using local_config_no_import/publish_config.py.
    The database and venues names are different and a capitalization
    typo is corrected.
    """
    for name in glob.glob('tmp_diff*'):  # clean old diff files
        os.remove(name)

    # The test is a Bash script, record output and put to file.
    # Must set PYTHONPATH in OS subprocess (sys.path cannot be
    # changed in this script - that has no effect on the OS subprocess)
    failure, output = subprocess.getstatusoutput(
        'export PYTHONPATH=local_config_publish_import:$PYTHONPATH; sh refs_demo.sh')

    if failure:
        print(output)
        raise OSError('test_config_no_import: could not run the test script run refs_demo.sh!')
    # Line with 'Saving invalid papers to ...' contains the date,
    # strip that off
    output = re.sub(r'^Saving invalid papers to.+$', '', output,
                    flags=re.MULTILINE)
    # User config...imported from... contains absolute path, strip off
    output = re.sub(r'^User configuration data imported from .+$', '', output,
                    flags=re.MULTILINE)
    f = open('refs_demo_with_local_config_no_import.out', 'w')
    f.write(output)
    f.close()
    # Strip off date and time in invalid_papers*.pub
    for filename in glob.glob('invalid_papers-*'):
        shutil.copy(filename, 'invalid_papers.pub')
    shutil.copy('publish_papers1.pub', 'publish_papers2.pub')
    shutil.copy('publish_venues1.txt', 'publish_venues2.txt')

    # Compare all files generated (incl. output from script)
    reference_data = 'reference_data'
    files = ['publish_papers2.pub', 'publish_venues2.txt',
             'refs_demo.sh',
             'refs_demo_with_local_config_no_import.out',
             'invalid_papers.pub',
             'present.html', 'present.bib']
    for filename in files :
        ref_file = os.path.join(reference_data, filename)
        failure = pydiff(ref_file, filename)
        success = not failure
        msg = """
New data in {} differs from reference data! Check out the files
tmp_diff*.txt (plain text comparison) or load tmp_diff*.html
into a browser for visual inspection of differences.
If differences are correct, run copy_new_reference_data.sh
to update the reference files.
""".format(filename)
        assert success, msg


def pydiff(files1, files2, n=3):
    """
    Use Python's difflib to compute the difference between
    files1 and files2 (can be corresponding lists of files
    or just two strings if only one set of files is to be
    compared).
    Produce text and html diff.
    """
    import difflib, time, os
    if isinstance(files1, str):
        files1 = [files1]
    if isinstance(files2, str):
        files2 = [files2]
    sizes = []  # measure diffs in bytes
    for fromfile, tofile in zip(files1, files2):

        if not os.path.isfile(fromfile):
            print(fromfile, 'does not exist')
            sys.exit(1)
        if not os.path.isfile(tofile):
            print(tofile, 'does not exist')
            sys.exit(1)

        fromdate = time.ctime(os.stat(fromfile).st_mtime)
        todate = time.ctime(os.stat(tofile).st_mtime)

        fromlines = open(fromfile, 'U').readlines()
        tolines = open(tofile, 'U').readlines()

        diff_html = difflib.HtmlDiff().make_file(
            fromlines, tolines, fromfile,tofile, context=True, numlines=n)
        diff_plain = difflib.unified_diff(
            fromlines, tolines, fromfile, tofile, fromdate, todate, n=n)
        filename_plain = 'tmp_diff_%s.txt' % tofile
        filename_html  = 'tmp_diff_%s.html' % tofile

        if os.path.isfile(filename_plain):
            os.remove(filename_plain)
        f = open(filename_plain, 'w')
        f.writelines(diff_plain)
        f.close()

        if os.path.isfile(filename_html):
            os.remove(filename_html)
        f = open(filename_html, 'w')
        f.writelines(diff_html)
        f.close()
        size = os.path.getsize(filename_plain)
        if size > 4:
            sizes.append(size)
        else:
            os.remove(filename_plain)
            os.remove(filename_html)
    # Return True if the files really differ,
    # diff in tmp_diff*.txt and tmp_diff*.html
    if sizes:
        return True
    else:
        return False

if __name__ == '__main__':
    test_demo()
    test_config_publish_import()
    test_config_no_import()
