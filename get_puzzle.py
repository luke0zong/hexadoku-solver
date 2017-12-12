def readHTML(level=1):
    import urllib.request
    pre = "http://www.sudoku-puzzles-online.com/cgi-bin/hexadoku/print-1-grid-hexadoku.cgi?"
    fp = urllib.request.urlopen(pre + str(level))
    my_bytes = fp.read()

    mystr = my_bytes.decode("utf8").splitlines()
    fp.close()

    myline = None
    for line in mystr:
        if line.startswith("</div><table id='table0'><tr><td>"):
            myline = line

    start = myline.find("<table id='grid'>") + len("<table id='grid'>")
    end = myline.find("</table>")
    my_grid = myline[start:end]

    grid_lines = my_grid.split('<tr>')
    puzzle = ''
    for l in grid_lines[1:]:
        l = l.replace('&nbsp;', '0').replace('<td>', '')
        puzzle += clean(l)

    return puzzle.replace('0', '.').lower()


def clean(s):
    import re
    s = re.sub("(<[^>]+>)", '', s)
    return s


def get_list(n, level=1):
    list = []
    while len(list) is not n:
        puzzle = readHTML(level)
        if puzzle not in list:
            list.append(puzzle)
    return list


def write_file(file_name, num, level=1):
    file = open(file_name, 'w')
    for item in get_list(num, level):
        file.write("%s\n" % item)


if __name__ == '__main__':
    # write_file("easy.txt", 25, 1)
    # write_file("mid.txt", 25, 2)
    # write_file("hard.txt", 25, 3)
    print(readHTML(2))
