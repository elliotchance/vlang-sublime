module main

fn test_something() {
	assert add(3, 5) == 10
}

fn test_interpolation() {
	one, two := 1, 2
	assert '1 + 2 \n = ${1 + 2} $one one' == "1 + 2 = 3"
	assert "$one + $two = 3" == "1 + 2 = 3"
}
