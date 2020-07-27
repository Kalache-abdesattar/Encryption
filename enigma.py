 #!/usr/bin/env python3
"""
	Enigma Implementation in python 3.7.6

"""

import random
import re 
import numpy as np


class Enigma:

	def generate_rotors(self):
		min_ascii_map = 65
		chars = 26 

		shift_values = [random.randint(1, chars), random.randint(1, chars), random.randint(1, chars)]

		rotor1 = dict([(i, chr((((i + shift_values[0]) % chars + min_ascii_map)))) for i in range(chars)])
		rotor2 = dict([(i, chr((((i + shift_values[1]) % chars + min_ascii_map)))) for i in range(chars)])
		rotor3 = dict([(i, chr((((i + shift_values[2]) % chars + min_ascii_map)))) for i in range(chars)])

		print('-------------------------------------KEEP THE ROUTERS!---------------------------------------')

		rotors = {'rotor 1' : rotor1,
				 'rotor 2' : rotor2,
				'rotor 3' : rotor3}

		return rotors


	def generate_plugboard(self, shuffle_rounds):
		min_ascii_map = 65
		max_ascii_map = 90

		plug_board = []

		chars = list(range(min_ascii_map, max_ascii_map))
		for _ in range(shuffle_rounds):
			np.random.shuffle(chars)

		for i in range(10):
			plug_board.append((chars[i], chars[-i-1]))

		plug = dict([(key, value) for key, value in plug_board])
		inversed_plug = dict([(value, key) for key, value in plug.items()])

		plug_board = {**plug, **inversed_plug}	

		print('-------------------------------------KEEP THE PLUG-BOARD!---------------------------------------')

		return plug_board


	def derive_init_state(self, enigma_key):
		# deriving rotors and the plug board from a single string
		# this can be usefull in a case of a shared connection
		# Where the enigma_key will behave as any asymmetric encryption
		# The enigma_key is shared by the Diffie-Hellan key exchange protocol

		assert(type(key) == type(''))
		key = key.strip().upper()

		regex_keys = re.compile(r'\d\d*')
		regex_values = re.compile(r'[A-Z]')

		keys = re.findall(key)
		keys = map(int, keys)
		values = re.findall(key)

		assert(len(keys) == len(values) == (26 * 3 + 10))
		assert(max(keys) == 25)

		rotor1 = dict([(k, v) for k, v in zip(keys[:26], values[:26])])
		rotor2 = dict([(k, v) for k, v in zip(keys[26:52], values[26:52])])
		rotor3 = dict([(k, v) for k, v in zip(keys[52:78], values[52:78])])

		plug = dict([(k, v) for k, v in zip(key[78:], values[78:])])
		inversed_plug = dict([(value, key) for key, value in plug.items()])

		plug_board = {**plug, **inversed_plug}

		rotors = {'rotor 1' : rotor1,
				 'rotor 2' : rotor2,
				'rotor 3' : rotor3}

		return tuple(rotors, plug_board)


	def enigma_encrypt(self, message, rotors, plug_board):
		# As the original Enigma Machine 
		# the code will encrypt messages after converting them to upper case and remove punctuations and spaces

		message = str(message).upper()

		regex = re.compile(r'[^A-Z]')
		message = regex.sub('', message)

		final_cipher = []
		r2 = r3 = 0
		
		rotor1 = rotors['rotor 1']
		rotor2 = rotors['rotor 2']
		rotor3 = rotors['rotor 3']
		arr = []
		for c in message:
			first_transition = rotor1.get(ord(c) % 65)
			second_transition = rotor2.get(ord(first_transition) % 65)
			third_transition = rotor3.get(ord(second_transition) % 65)
			arr.append(third_transition)
			c = chr(plug_board.get(ord(third_transition), ord(third_transition)))
			
			final_cipher.append(c)
			r2 += 1
				
			rotor1 = dict([((i+1) % 26, v) for i, v in rotor1.items()])   #rotating rotor 1     

			if r2 == 26:
				r2 = 0
				r3 += 1
				rotor2 = dict([((i+1) % 26, v) for i, v in rotor2.items()])     #rotating rotor 2 when rotor 1 finishes complete cycle

				if r3 == 26:
					r3 = 0
					r3 += 1
					rotor3 = dict([((i+1) % 26, v) for i, v in rotor3.items()])       #rotating rotor 3 when rotor 2 finishes complete cycle

		message = "".join(final_cipher)
		
		return message	
 

	def enigma_decrypt(self, encryted_message, rotors, plug_board):
		# The decrypted message will be returned as 
		# upper case with no space or punctuations 

		min_ascii_map = 65

		message = str(encryted_message).upper()

		regex = re.compile(r'[^A-Z]')
		message = regex.sub('', message)

		final_cipher = []
		r2 = r3 = 0

		rotor1 = dict([(value, key % 26) for key, value in rotors['rotor 1'].items()])
		rotor2 = dict([(value, key % 26) for key, value in rotors['rotor 2'].items()])
		rotor3 = dict([(value, key % 26) for key, value in rotors['rotor 3'].items()])

		for c in encryted_message:
			plug_transition = plug_board.get(ord(c), ord(c))

			array.append(chr(plug_transition))
			third_transition = rotor3.get(chr(plug_transition))
			second_transition = rotor2.get(chr(third_transition + min_ascii_map))
			first_transition = rotor1.get(chr(second_transition + min_ascii_map))

			c = chr(first_transition + min_ascii_map)

			final_cipher.append(c)
			r2 += 1

			rotor1 = dict([(i, (v+1) % 26) for i, v in rotor1.items()])

			if r2 == 26:
				r2 = 0
				r3 += 1	
				rotor2 = dict([(i, (v+1) % 26) for i, v in rotor2.items()])

				if r3 == 26:
					r3 = 0
					r3 += 1
					rotor3 = dict([(i, (v+1) % 26) for i, v in rotor3.items()])		
	
		message = "".join(final_cipher)
		
		return message		



def main():
	enigma = Enigma()

	rotors = enigma.generate_rotors()
	plug_board = enigma.generate_plugboard(10000)


	print('''
				########    #     #     ###     #########     #       #           #
				#  			##    #      #		#			  ##	 ##          # #
				#			# #   #      #		#			  # #   # #         #   #
				########	#  #  #      #		#    ####     #  # #  #        #######
				#			#   # #      # 		#       #     #   #   #       #       #
				#		    #    ##      #		#       #     #       #      #         #
				########    #     #     ###		#########     #       #     #           #
		''')


	message = input('Enter A Message : ')
	choice = input('Encrypt or Decrypt ? (e/d) : ')
	
	if choice.lower() == 'e':
		encrypted_message = enigma.enigma_encrypt(message, rotors, plug_board)
		print(f'The Encrypted Message : {encrypted_message}')

	elif choice.lower() == 'd':
		decrypted_message = enigma.enigma_decrypt(message, rotors, plug_board)
		print(f'The Encrypted Message : {decrypted_message}')	



if __name__ == "__main__" :
	main()	
