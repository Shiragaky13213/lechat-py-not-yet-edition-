#!python3
# -*- coding: utf-8 -*-
########################################
# capsolver.py
# solves basic and intermediate captchas (not yet advanced)
# credits to @ninja at dan's chat for this captcha solving method



from PIL import Image
from io import BytesIO
import imagehash



# solve a basic captcha
def solver(captcha):
	capdebug = 0
	capfile = BytesIO(captcha)  # convert image to file-like object
	MARGIN_LEFT = 5
	MARGIN_TOP = 8
	CHAR_WIDTH = 8
	CHAR_HEIGHT = 12
	KERNING = 1
	split_chars = []
	#
	CHARS = {
		7500661077491839778768289792		: 		'0',
		7495907210046667157753692160		: 		'1',
		18693331940121537961265135616		: 		'2',
		38615522809929702947329671168		: 		'3',
		1873977694927228329060073472		: 		'4',
		78842217021210158637042630656		: 		'5',
		18693330719671560339701104640		: 		'6',
		78922318560553249183541231616		: 		'7',
		18693333770265832732399239168		: 		'8',
		18693335488899193051031535616		: 		'9',
		#
		1150832819283519275008				:		'a',
		59654146412341018680025153536		: 		'b',
		1150886089507806773248				: 		'c',
		932097069857263101880762368		: 		'd',
		1114209687836664135680				: 		'e',
		9346447241104789231094464512		: 		'f',
		2320238420711738098558				: 		'g',
		59654146412341018679436312576		: 		'h',
		7456655490136865025443102720		: 		'i',
		1864163872534216256371738236		: 		'j',
		29827073058098511562936614912		: 		'k',
		17360288550919685737411248128		: 		'l',
		3373149919266677129216				: 		'm',
		4074912045710853734400				: 		'n',
		1114209621878901571584				: 		'o',
		4074912045711442624704				: 		'p',
		1095834935399246660355				: 		'q',
		4103490935242696425472				: 		'r',
		2338395165874957713408				: 		's',
		58259764984514814439981056			: 		't',
		3611221428075235049472				: 		'u',
		3611195148067275276288				: 		'v',
		3611228209968587341824				: 		'w',
		3604481884111535013888				: 		'x',
		3611221428075235083134				: 		'y',
		2324725503147407966208				: 		'z',
		#
		7500661077491906151174045696		: 		'A',
		78230514319396601059115532288		: 		'B',
		19308669237460611730629328896		: 		'C',
		78230514259948241552894853120		: 		'D',
		78842216506339998208943325184		: 		'E',
		79151701516161343277664043008		: 		'F',
		19308664515096102492945907712		: 		'G',
		60586241926996184390279823360		: 		'H',
		39024239238413840548150247424		: 		'I',
		9291832294871442810541178880		: 		'J',
		60589911592066825244343730176		: 		'K',
		59654145893093148305731223552		: 		'L',
		60630047038625823002386956288		: 		'M',
		60625155109671441030361317376		: 		'N',
		18693335495566983955341901824		: 		'O',
		78845857506382638114603532288		: 		'P',
		18693335495567010395160641536		: 		'Q',
		78845857506398413933259194368		: 		'R',
		39231762017534009060913709056		: 		'S',
		78947805505367354413640318976		: 		'T',
		60586241922672728746435018752		: 		'U',
		60586240200397847457884012544		: 		'V',
		60586241924408893050936557568		: 		'W',
		60585800239909242285204897792		: 		'X',
		60585800239909202364898738176		: 		'Y',
		78616474606842160770308767744		: 		'Z'}
	#
	def extract_chars(target_cap):
		cap = Image.open(target_cap).convert("P")
		split_chars = [		cap.crop((5, 8, 13, 20)),
							cap.crop((14, 8, 22, 20)),
							cap.crop((23, 8, 31, 20)),
							cap.crop((32, 8, 40, 20)),
							cap.crop((41, 8, 49, 20))]
		return split_chars
	#
	def image_to_int(im):
		n = 0
		for bit in im.getdata():
			n <<= 1
			n += bit
		return n
	#
	def int_to_image(n):
		im = Image.new('1', (CHAR_WIDTH, CHAR_HEIGHT))
		bits = []
		for _ in range(CHAR_WIDTH * CHAR_HEIGHT):
			bits.append(n & 1)
			n >>= 1
		bits.reverse()
		im.putdata(bits)
		return im
	#
	def hamming_distance(n1, n2):
		d = 0
		while n1 or n2:
			d += (n1 & 1) ^ (n2 & 1)
			n1 >>= 1
			n2 >>= 1
		return d
	#
	def guess_character(im):
		n = image_to_int(im)
		if(capdebug>0): print(str(n))
		guess = min(CHARS, key=lambda c: hamming_distance(c, n))
		return CHARS[guess]
	#
	def guess_captcha(split_chars):
		chars = []
		for target in split_chars:
			char = guess_character(target)
			chars.append(char)
		return ''.join(chars)
	#
	def solve_captcha(target_cap):
		split_chars = extract_chars(target_cap)
		solution = guess_captcha(split_chars)
		if(capdebug>0): print(solution)
		return solution
	#
	solution = solve_captcha(capfile)
	#
	return solution
#



###############################
# End of file