// This file is included as a way to test commands with a V file.

module main

import os

#flag -lsqlite3
#include "sqlite3.h"

[unsafe]
struct Foo {
	bar int
	baz string
}

pub interface Writer {
	write() ?f64
}

fn (foo Foo) write() ?f64 {
	return -1.23 * 0xAF
}

enum Color {
	red
	green
	blue
}

fn main() {
	mut a := 4 + 5
	b := 6
	println(a)

	foo := Writer(Foo{})
	if foo is Writer {
		println(foo)
	}

	$if windows {
		bar := Foo{}
		println(bar as Foo)
		println(@LINE)
	}

	mut color := Color.red
	color = .green
	println(color) // "green"
	match color {
		.red { println('the color was red') }
		.green { println('the color was green') }
		.blue { println('the color was blue') }
	}
}

fn add(a int, b int) int {
	return a + b
}
