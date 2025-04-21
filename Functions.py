from time import strftime as format_time_str, localtime as to_time_struct, strptime as parse_time_str, mktime as to_secs

dateTimeFmt = "%m/%d/%Y %I:%M %p"

def sanitary_eval(expr, locals = {}):

	code = compile(expr, "<string>", "eval")
	for name in code.co_names:

		if name not in locals:

			allowedNames = list(locals.keys())
			if allowedNames != []:

				raise NameError(
					f"\"{name}\" is an illegal name for evaluations. The only names allowed in evaluations are {allowedNames}."
				)

			else:

				raise NameError(
					f"\"{name}\" is an illegal name for evaluations. There are no names allowed in these evaluations."
				)

	return eval(code, {"__builtins__": {}}, locals)

def secs_to_str(secs):

	return format_time_str(dateTimeFmt, to_time_struct(secs))

def str_to_secs(str):

	return to_secs(parse_time_str(str, dateTimeFmt))