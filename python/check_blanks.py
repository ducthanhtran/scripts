import argparse


def is_blank(line):
    return line == ""


def smart_open(file_path):
    import os
    ending = os.path.splitext(file_path)[1]
    if ending == '.gz':
        import gzip
        return gzip.open(file_path, 'rt')
    else:
        return open(file_path, 'r')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--left', type=str, required=True)
    parser.add_argument('--right', type=str, required=True)

    args = parser.parse_args()

    number_blank = 0
    missmatch = 0
    with smart_open(args.left) as inp_left, smart_open(args.right) as inp_right:
        for index, (line_left, line_right) in enumerate(zip(inp_left, inp_right)):
            line_left = line_left.rstrip()
            line_right = line_right.rstrip()

            left_is_blank = is_blank(line_left)
            right_is_blank = is_blank(line_right)
            if not (left_is_blank == right_is_blank):
                print("Line {} has mismatch: {} vs. {}".format(index, left_is_blank, right_is_blank))
                missmatch += 1
            if left_is_blank and right_is_blank:
                number_blank += 1

    print("Missmatches: {}".format(missmatch))
    print("Number of correct blanks: {}".format(number_blank))
