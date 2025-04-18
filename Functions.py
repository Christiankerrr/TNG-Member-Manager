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