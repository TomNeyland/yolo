#! /usr/bin/env python
import re
import os
import json
import configargparse
import simplejson as json

from git import Repo, InvalidGitRepositoryError

YOLO_TAG_REGEX = re.compile(
    '[ \t]*(#|(/\*)|(//)|(\<\!\-\-)) yolo, (?P<reason>[^\n]*)')
SORRY_TAG_REGEX = re.compile('[ \t]*(#|(/\*)|(//)|(\<\!\-\-)) sorry')


def main():
    options = get_options()
    yolo_results = [yolo(sourcefile)
                    for sourcefile in options.sourcefiles]

    if len(yolo_results) is 1:
        print json.dumps(yolo_results[0], cls=GitObjectEncoder)
    else:
        print json.dumps(yolo_results, cls=GitObjectEncoder)


# yolo, these options are just mocked up
def get_options():
    options_parser = configargparse.ArgParser(
        default_config_files=['./.yolorc'])

    options_parser.add('-c', '--config', required=False, is_config_file=True,
                       env_var='YOLO_CONFIG', help='config file path')

    options_parser.add('--repo', default='./', required=False,
                       help='the git repo running yolo on')

    options_parser.add('sourcefiles', nargs='+',
                       help='the sourcefile(s) to run yolo on')

    return options_parser.parse_args()
# sorry


# yolo, we can decide field names later
def yolo(filename):

    with open(filename, 'rb') as sourcefile:

        yolo_blocks = find_yolo_blocks(sourcefile)
        repo = find_git_repo(filename)

        yolo_data = {
            'yolo_blocks': yolo_blocks,
            'yolo_count': len(yolo_blocks)
        }

        if repo:
            blame_data = get_blame_data(repo, 'HEAD', filename)
            line_number = 1
            for yolo_block in yolo_blocks:
                for line_info in yolo_block['lines']:
                    line_info['blame'] = blame_data[line_info['line_number']]

            yolo_data['authors'] = list(set(commit.author
                                            for commit in blame_data.values()))

    return yolo_data
# sorry


# yolo, wip implementation
def find_yolo_blocks(sourcefile):

    yolo_blocks = []

    source_lines = enumerate(sourcefile, 1)

    for line_number, source_line in source_lines:

        if is_yolo_tag(source_line):

            reason = YOLO_TAG_REGEX.match(source_line).groupdict()['reason']
            start_line_number = line_number + 1

            # start grabbing the yoloed lines, look for a sorry tag
            yoloed_lines = []

            for yoloed_line_number, yoloed_line in source_lines:

                if is_sorry_tag(yoloed_line):

                    end_line_number = yoloed_line_number - 1

                    yolo_blocks.append({
                        'reason': reason,
                        'start_line_number': start_line_number,
                        'end_line_number': end_line_number,
                        'lines': yoloed_lines
                    })

                    break  # back to looking for yolo tags

                else:
                    yoloed_lines.append({
                        'line': yoloed_line,
                        'line_number': yoloed_line_number
                    })

    return yolo_blocks
# sorry


def find_git_repo(filename):

    path = os.path.abspath(filename)

    while path is not '/':
        path = os.path.dirname(path)
        try:
            return Repo(path)
        except InvalidGitRepositoryError:
            continue


def get_blame_data(repo, rev, sourcefile):
    lines_by_commit = repo.blame(rev, sourcefile)
    line_number = 1

    blame_data = {}

    for commit, lines in lines_by_commit:
        for line in lines:
            blame_data[line_number] = commit
            line_number += 1

    return blame_data


def is_yolo_tag(source_line):
    return YOLO_TAG_REGEX.match(source_line) is not None


def is_sorry_tag(source_line):
    return SORRY_TAG_REGEX.match(source_line) is not None


class GitObjectEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (set,)):
            return [self.default(o) for o in obj]
        if hasattr(obj, '__slots__'):
            data = {key: getattr(obj, key)
                    for key in obj.__slots__ if hasattr(obj, key)}
            return data
        else:
            return super(GitObjectEncoder, self).default(obj)


if __name__ == '__main__':
    main()
