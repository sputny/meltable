#!/usr/bin/env python3
# coding=<utf-8>
"""
usage:
    meltable [-v -o]  <file> ...

options:
    -v      Be verbose.
    -o      Override existing files.
"""
import PyPDF2 as pdf
import docopt
import re
import os


def main():
    args = docopt.docopt(__doc__)
    team, athlets = parse_pdf(args)
    team_filename = "team.csv"
    athlet_filename = "athlet.csv"
    if args['-o'] or not(
            os.path.exists(team_filename) or os.path.exists(athlet_filename)):
        save_csv(team_filename, team)
        save_csv(athlet_filename, athlets)


def parse_pdf(args):
    filenames = args['<file>']
    team = []
    athlets = []
    team_regex = re.compile(r"^u(\d)$")
    athlet_re = re.compile(r"^vn(\d)(\d\d?)$")
    for filename in filenames:
        reader = pdf.PdfFileReader(filename)
        text = reader.getFormTextFields()
        for n, t in enumerate([team_regex.match(key)
                               for key in text
                               if team_regex.match(key)]):
            var = [
                text['vereinsnr'], text['u' + t.group(1)],
                text['t' + t.group(1)], text['tn' + t.group(1)], '']
            if args['-v'] and all([x == '' for x in var[1:4]]):
                print("Auf Meldung {} ist Team {} nicht befüllt".format(
                    filename, n))
            elif args['-v'] and any([x == '' for x in var[1:4]]):
                print("Auf Meldung {} ist Team {}"
                      + " nicht vollständing befüllt".format(filename, n))
            else:
                team.append(var)
            for k, a in enumerate([
                    athlet_re.match(key)
                    for key in text
                    if athlet_re.match(key)
                    and athlet_re.match(key).group(1) == t.group(1)]):
                a_var = [
                        text['n' + a.group(1) + a.group(2)],
                        text['vn' + a.group(1) + a.group(2)],
                        text['jg' + a.group(1) + a.group(2)],
                        text['vereinsnr'], text['tn' + a.group(1)]]
                if args['-v'] and all([x == '' for x in a_var[:3]]):
                    print("Auf Meldung {} Teilnehmer {} ".format(filename, k)
                          + "von Team {} nicht befüllt".format(n + 1))
                elif args['-v'] and any([x == '' for x in a_var[:3]]):
                    print("Auf Meldung "
                            + "{} Teilnehmer {} von Team {} nicht".format(
                                filename, k, n)
                            + " vollständing befüllt")
                else:
                    athlets.append(a_var)
    return team, athlets


def save_csv(name, content):
    with open(name, 'w') as f:
        [f.writeline(";".join(x)+ "\n") for x in content]
