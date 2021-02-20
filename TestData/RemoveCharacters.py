# Remove special characters (",whitespace etc.) on csv file

s = open('./December.csv', 'r').read()

chars = ('"',' ') # etc
for c in chars:
  s = ''.join( s.split(c) )

out_file = open('Cleaned.csv', 'w')
out_file.write(s)
out_file.close()