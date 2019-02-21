#!/usr/bin/env python3
# coding=<utf-8>
import PyPDF2 as pdf
import argparse
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-o', tpye=argparse.FileType('w'),
            help="name of output file")


def parse_pdf(filenames):
    if isinstance(filenames, str):
        filenames = [filenames]
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
            if all([x == '' for x in var[1:4]]):
                print("Auf Meldung {} ist Team {} nicht befüllt".format(
                    filename, n))
            elif any([x == '' for x in var[1:4]]):
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
                if all([x == '' for x in a_var[:3]]):
                    print("Auf Meldung {} Teilnehme {} "
                          + "von Team {} nicht befüllt".format(filename, k, n))
                elif any([x == '' for x in a_var[:3]]):
                    print("Auf Meldung {} Teilnehme {} von Team {} nicht"
                          + " vollständing befüllt".format(filename, k, n))
                else:
                    athlets.append(a_var)
    return team, athlets
