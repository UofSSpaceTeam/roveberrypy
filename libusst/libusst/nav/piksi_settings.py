
def boolify(s):
	if s == "True":
		return True
	elif s == "False":
		return False
	else:
		raise ValueError("Not a boolean")
		
def autocast(s):
    for fn in (boolify, int, long, float, str):
        try:
            return fn(s)
        except ValueError:
            pass
    return s
	

valid_calls = { \
	"simulator" : { "enabled" : (bool), "radius" : (int, long, float) } \
}

def validate(arg0, arg1, arg2):
	global valid_calls
	if arg0 in valid_calls and arg1 in valid_calls[arg0]:
		try:
			if isinstance(autocast(arg2), valid_calls[arg0][arg1]):
				return True
			else:
				return False
		except:
			return False
	else:
		return False