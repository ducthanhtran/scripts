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


def output(document_left, document_right, output_file_left, output_file_right):
    for doc_l, doc_r in zip(document_left, document_right):
        output_file_left.write(doc_l + "\n")
        output_file_right.write(doc_r + "\n")
    output_file_left.write("\n")
    output_file_right.write("\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--left', type=str, required=True)
    parser.add_argument('--right', type=str, required=True)
    parser.add_argument('--out-left', type=str, required=True)
    parser.add_argument('--out-right', type=str, required=True)

    args = parser.parse_args()

    with smart_open(args.left) as inp_left, smart_open(args.right) as inp_right, \
         open(args.out_left, 'w') as out_left, open(args.out_right, 'w') as out_right:

        doc_left = []
        doc_right = []
        search_for_next_blank_start = False
        for index, (line_left, line_right) in enumerate(zip(inp_left, inp_right)):
            line_left = line_left.rstrip()
            line_right = line_right.rstrip()

            ibl = is_blank(line_left)
            ibr = is_blank(line_right)
            if ibl and ibr:
                if search_for_next_blank_start:
                    search_for_next_blank_start = False
                else:
                    output(doc_left, doc_right, out_left, out_right)
                    doc_left[:] = []
                    doc_right[:] = []

            elif ibl != ibr:
                output(doc_left, doc_right, out_left, out_right)
                doc_left[:] = []
                doc_right[:] = []
                search_for_next_blank_start = True
            else:
                if not search_for_next_blank_start:
                    doc_left.append(line_left)
                    doc_right.append(line_right)
