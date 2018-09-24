from copy import deepcopy
from typing import List, Tuple, Callable

Tape = Tuple[int, int, int, List[int]]
Stack = List[int]
App = Tuple[int, List[str]]

def interactive_mode():
	tape = make_tape(size=16)
	app = make_app()
	while True:
		command = input()
		app = append_commands( app, command )
		while not at_end(app):
			task = current_instruction( app )
			tape, app = task( tape, app )
			app = increment_command_index( app )

def current_instruction( app: App ) -> Callable:
	return parse_command( get_command( app ) )

def parse_command( command: str ) -> Callable:
	if command == ">": return move_right
	if command == "<": return move_left
	if command == ".": return output_num
	if command == "!": return output_ascii
	if command == "+": return increment_cell
	if command == "-": return decrement_cell
	if command == "]": return end_loop
	if command == "[": return begin_loop
	if command == ",": return read_input
	return noop

def read_input( tape: Tape, app: App ):
	return set_value( tape, ord( input("Enter char:") ) ), app

def add_instruction( app: App ) -> App:
	commands = deepcopy( app[1] )
	return app[0], commands

def noop(tape: Tape, app: App) -> Tuple[Tape, App]:
	return tape, app

def move_left(tape: Tape, app: App) -> Tuple[Tape, App]:
	if get_index(tape) > 0:
		return (tape[0], tape[1], get_index(tape) - 1, tape[3]), app
	else:
		return (tape[0], tape[1], get_size(tape) - 1, tape[3]), app

def move_right(tape: Tape, app: App) -> Tuple[Tape, App]:
	if get_index(tape) < get_size(tape) - 1 :
		return (tape[0], tape[1], get_index(tape) + 1, tape[3]), app
	else:
		return (tape[0], tape[1], 0, tape[3]), app

def increment_cell( tape: Tape, app: App ) -> Tuple[Tape, App]:
	if get_value(tape) < get_max_value(tape):
		return set_value( tape,  get_value(tape) + 1), app
	else:
		return tape, app

def decrement_cell( tape: Tape, app: App ) -> Tuple[Tape, App]:
	if get_value(tape) > 0 :
		return set_value( tape,  get_value(tape) - 1), app
	else:
		return tape, app

def output_num( tape: Tape, app: App ) -> Tuple[Tape, App]:
	print( get_value( tape ) )
	return tape, app

def output_ascii( tape: Tape, app: App ) -> Tuple[Tape, App]:
	print( chr( get_value( tape ) ) )
	return tape, app

def end_loop( tape: Tape, app: App ) -> Tuple[Tape, App]:
	if get_value( tape ) == 0:
		return tape, app
	else:
		open_loops = 1
		while open_loops > 0:
			app = decrement_command_index( app )
			if get_command( app ) == "]":
				open_loops += 1
			elif get_command( app ) == "[":
				open_loops -= 1
		return tape, app


def begin_loop( tape: Tape, app: App ) -> Tuple[Tape, App]:
	if get_value( tape ) != 0:
		return tape, app
	else:
		open_loops = 1
		while open_loops > 0:
			app = increment_command_index( app )
			if get_command( app ) == "[":
				open_loops += 1
			elif get_command( app ) == "]":
				open_loops -= 1
		return tape, app

def make_app() -> App:
	return 0, []

def append_command( app: App, command: str ) -> App:
	commands = deepcopy( app[1] )
	commands.append( command )
	return app[0], commands

def append_commands( app: App, new_commands: str ) -> App:
	commands = deepcopy( app[1] )
	for command in new_commands:
		commands.append( command )
	return app[0], commands

def get_app_index( app: App ) -> App:
	return app[0]

def at_end( app: App ) -> bool:
	return get_app_index( app ) == len( app[1] )

def get_command( app: App ) -> str:
	return app[1][ get_app_index( app ) ]

def get_command_count(app: App) -> int:
	return len(app[1])

def increment_command_index( app: App ) -> App:
	if get_app_index(app) < get_command_count(app):
		return get_app_index(app) + 1, app[1]
	else:
		return app

def decrement_command_index( app: App ) -> App:
	if get_app_index(app) > 0:
		return get_app_index(app) - 1, app[1]
	else:
		return app

def make_tape(size: int = 255, max_value: int = 255, index: int = 0) -> Tape:
	return size, max_value, 0, [0]*(size+1)

def get_size( tape: Tape ) -> int:
	return tape[0]

def get_max_value( tape: Tape ) -> int:
	return tape[1]

def get_index( tape: Tape ) -> int:
	return tape[2]

def get_value( tape: Tape ) -> int:
	return tape[3][ get_index(tape) ]

def set_index( tape: Tape, index: int ) -> Tape:
	return tape[0], tape[1], index, tape[3]

def set_value( tape: Tape, value: int ) -> Tape:
	values = deepcopy(tape[3])
	values[get_index(tape)] = value
	return tape[0], tape[1], tape[2], values

interactive_mode()