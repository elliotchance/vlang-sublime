// SYNTAX TEST "Packages/V/V.sublime-syntax"

module main
// ^^^^ keyword.operator.word.v

import os
// ^^^ meta.import.v keyword

#flag -lsqlite3
// ^^ meta.flag.v keyword.flag.v
#include "sqlite3.h"
// ^^^^^^ meta.include.v keyword.include.v

[unsafe]
// ^^^^ storage.modifier.v
struct Foo {
// ^^^ keyword
	bar int
	baz string
    // ^^^^ storage.type.v
}

pub interface Writer {
	write() ?f64
}

fn (foo Foo) write() ?f64 {
// <- keyword
	return -1.23 * 0xAF
// ^^^^ keyword.control.v
}

enum Color {
// <- keyword
	red
	green
	blue
}

fn main() {
	mut a := 4 + 5
    // ^^ operator
	b := 6
	println(a)

	foo := Writer(Foo{})
	if foo is Writer {
		println(foo)
	}
    // ^ comment.line.v punctuation.definition.comment.v

	$if windows {
// ^ keyword.control.v
		bar := Foo{}
		println(bar as Foo)
		println(@LINE)
        // ^^^^ variable.language.v
	}

	mut color := Color.red
    // ^^^ variable.other.readwrite
	color = .green
	println(color) // "green"
	match color {
		.red { println('the color was red') }
// ^^^ entity.name.constant.v
		.green { println('the color was green') }
		.blue { println('the color was blue') }
    // <- entity.name.constant.v
	}
}

fn add(a int, b int) int {
// ^^^ entity.name.function.v
	return a + b
// ^^^^ keyword.control.v
}

fn test_something() {
    assert add(3, 5) == 10
    // ^^^ keyword.control.v
}

fn test_interpolation() {
// ^^^^^^^^^^^^^^^^^^ entity.name.function.v
    one, two := 1, 2
    // ^ punctuation.delimiter.comma.v
    assert '1 + 2 \n = ${1 + 2} $one one' == "1 + 2 = 3"
    // <- keyword.control.v
    assert "$one + $two = 3" == "1 + 2 = 3"
}
