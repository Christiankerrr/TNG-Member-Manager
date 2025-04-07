def sanitary_eval(expr, locals = {}):

	code = compile(expr, "<string>", "eval")
	for name in code.co_names:

		if name not in locals:

			raise NameError

	return eval(code, {"__builtins__": {}}, locals)