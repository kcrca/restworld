import csv

dest = r'E:\ETHICON_EXPORT'
out = open("build.bat", "w")
with open('in.csv', 'rb') as raw:
    rows = tuple(csv.reader(raw))
    count = '{:,}'.format(len(rows))
    dirs = {}
    for i, row in enumerate(rows):
        if i == 0:
            continue
        path, id, name = row
        name = name.strip()
        parts = path.split('>')
        dir = '\\'.join(parts[1:-1])
        if dir not in dirs:
            out.write(r'mkdir "%s\%s"%s' % (dest, dir, "\n"))
            dirs[dir] = True
        out.write(r'copy "E:\ETHICON_STORAGE\storage\000\%03d\%03d\%s" "%s\%s\%s"%s' % (
            int(id) / 1000, int(id), name, dest, dir, name, "\n"))
        out.write("if %errorlevel% neq 0 exit /b %errorlevel%\n")
        out.write('echo %s files of %s, %.1f%%%%\n' % ('{:,}'.format(i + 1), count, (i + 1) * 100.0 / len(rows)))
