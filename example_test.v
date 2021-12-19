module main

fn test_something() {
	assert add(3, 5) == 7
}

fn test_interpolation() {
	one, two := 1, 2
	assert '1 + 2 = ${1 + 2}' == "1 + 2 = 4"
	assert "$one + $two = 3" == "1 + 2 = 3"
}

fn test_hi() {
	assert 1 == 1
}
