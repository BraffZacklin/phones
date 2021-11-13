from random import choice

'''
def expandStructures(string):
	if if "(" not in string and if ")" not in string:
		return string

	expanded_structures = []
	more_structures = True
	while more_structures:
		if "(" in string and if ")" in string:

		elif "(" in string or if ")" in string:
			raise ValueError, "missing opening or closing bracket in structures directive"
		else:
			more_structures = False
	return expanded_structures
'''

class Reader():
	def __init__(self, textfile, outfile="./outfile.txt"):
		self.outfile = outfile
		self.textfile_list = []
		self.textfile = textfile
		self.consonants = []
		self.vowels = []
		self.structures = []
		self.disallowed = []
		self.reader_dictionary = {}
		self.max_syllables = False
		self.wordbank = []
		self.readDictionaryFile()

	def returnDirectives(self):
		return self.consonants, self.vowels, self.structures, self.disallowed, self.max_syllables

	def removeComments(self, string):
		if "//" in string:
			return string[:string.index("//")]
		return string

	def findDirectiveName(self, line):
		return line.split()[0]

	def processListDirective(self, line):
		line = line.replace(self.findDirectiveName(line), "")
		#return [(self.removeComments(n).strip()) for n in line.split(",")]
		return [(n.strip()) for n in line.split(",")]

	def readDictionaryFile(self):
		with open(self.textfile, "r") as file:
			self.textfile_list = file.readlines()
			for index, line in enumerate([line.strip() for line in self.textfile_list if line.strip() != ""], start=1):
				if line[0:2] == "//":
					continue
				line = self.removeComments(line)
				if line[0] == "#":
					try:
						if "CONSONANTS" in line:
							self.consonants = self.processListDirective(line)
						elif "VOWELS" in line:
							self.vowels = self.processListDirective(line)
						elif "STRUCTURES" in line:
							self.structures = self.processListDirective(line)
						elif "DISALLOWED" in line:
							self.disallowed = self.processListDirective(line)
						elif "MAX_SYLLABLES" in line:
							self.max_syllables = line.replace(self.findDirectiveName(line), "")
							self.max_syllables.strip()
							self.max_syllables = int(self.max_syllables)
					except ValueError as e:
						print(e)
						print(f'foanz: mangled directive on line {index}')
						print(f'\t"{line}"')
						quit()
				elif ":" in line:
					if line[0].isdigit() or line[0] == "?":
						line = [line.strip() for line in line.split(":")]
						if line[0] == "?" and self.max_syllables == False:
							print(f'foanz: MAX_SYLLABLES not defined but wildcard is used on line {index}')
							print(f'\t{line}')
							quit()

						if line[0] in self.reader_dictionary:
							self.reader_dictionary[line[0]].append(line[1])
						else:
							self.reader_dictionary[line[0]] = [line[1]]
					elif line[0:5] == "bank:":
						line = line.replace("bank:", "")
						line = line.strip()
						self.wordbank.append(line)

		return self.reader_dictionary

	def defineWord(self, word, definition):
		if "." in word:
			word = word.replace(".", "")
		for index, line in enumerate(self.textfile_list):
			if definition in line:
				line_list = line.split(":")
				line_list[0] = f'{word} ({line_list[0]})'
				line_list = ":".join(line_list)
				self.textfile_list[index] = line_list

	def addWord(self, word):
		syllables = 1
		for char in word:
			if char == ".":
				syllables = syllables+1
		syllables = str(syllables)
		if syllables in self.reader_dictionary:
			definition = choice(self.reader_dictionary[syllables])
			print(definition)
			self.defineWord(word, definition)
			self.reader_dictionary[syllables].remove(definition)
			if not self.reader_dictionary[syllables]:
				del self.reader_dictionary[syllables]
			return None
		elif "?" in self.reader_dictionary:
			self.defineWord(word, choice(self.reader_dictionary["?"]))
			return None
		else:
			for key in self.reader_dictionary.keys():
				if "-" in key:
					syllables = int(syllables)
					syllable_range = key.split("-")
					if syllables in range(syllable_range[0], syllable_range[1]):
						defineWord(word, choice(self.reader_dictionary[key]))
			return None
		return word

	def save(self, wordbank):
		with open(self.outfile, "w+") as file:
			for line in self.textfile_list:
				file.write(line)
			file.write("\n\n")
			for line in self.wordbank:
				file.write(f'bank: {line}\n')

if __name__ == "__main__":
	reader = Reader("./example.txt")
	reader.readDictionaryFile()
	print(reader.reader_dictionary)
	reader.defineWord("hi", "This word will be one syllable")
	reader.save()